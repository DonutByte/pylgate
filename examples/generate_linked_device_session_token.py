# This program is dedicated to the public domain under the Creative Commons Attribution 3.0 Unported License.

"""
This program generates a new session token as a Linked Device.

For detailed explanation on Device Linking, go to https://www.pal-es.com/tutorials

Note:
you must install pylgate via:
`pip install git+https://github.com/DonutByte/pylgate.git@main`

And install `qrcode` and `requests` via
`pip install qrcode requests`
"""
import time
import traceback
import uuid
from urllib.parse import urljoin
from typing import Any

import qrcode
import requests

import pylgate
from pylgate.types import TokenType

ANDROID_USER_AGENT = 'okhttp/4.9.3'
BASE_URL = 'https://api1.pal-es.com/v1/bt/'


def main():
    try:
        phone_number, session_token, token_type = login_via_device_linking()
        print('Logged-in successfully :)')
        print(f'Phone number (user id): {phone_number}')
        print(f'Session token: {session_token.hex()}')
        print(f'Token type: {token_type} (TokenType.{token_type.name})')
    except Exception:
        print('Failed to login.\n'
              'To get help please open an issue here https://github.com/DonutByte/pylgate/issues/new/choose\n'
              'Please provide the following traceback and any additional info that might help:')
        traceback.print_exc()
        exit(1)


def login_via_device_linking() -> (int, bytes, TokenType):
    print('Logging-in via Device Linking, Please open your palgate app and scan this QR code:')
    phone_number, session_token, token_type = start_device_linking()

    print('checking status...')
    check_status(phone_number, session_token, token_type)

    """
    In palgate app version 1.6.0046 GatesFragment was changed to only update user details if it wasn't already updated ("filterUploaded" in preferences)
    This caused a bug (see https://github.com/DonutByte/pylgate/issues/19) where our request was denied by the server
    """
    # print('updating user info...')
    # update_user(phone_number, session_token, token_type)

    print('checking derived token...')
    check_token(phone_number, session_token, token_type)

    return phone_number, session_token, token_type


def start_device_linking() -> (int, bytes, TokenType):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    unique_id = uuid.uuid4()
    qr.add_data(f'{{"id": "{unique_id}"}}')
    qr.make(fit=True)

    qr.print_ascii(invert=True)

    response = requests.get(
        urljoin(BASE_URL, f'un/secondary/init/{unique_id}'),
        headers=_basic_headers(),
    )

    response_data = _validate_response(response)
    phone_number = int(response_data['user']['id'])
    session_token = bytes.fromhex(response_data['user']['token'])
    token_type = TokenType(int(response_data['secondary']))

    return phone_number, session_token, token_type


def check_status(phone_number: int, session_token: bytes, token_type: TokenType) -> None:
    status_response = requests.get(urljoin(BASE_URL, 'secondary/status'),
                                   headers=_get_authenticated_headers(phone_number, session_token, token_type))

    _ = _validate_response(status_response)


def update_user(phone_number: int, session_token: bytes, token_type: TokenType) -> None:
    update_response = requests.put(urljoin(BASE_URL, 'user'),
                                   data={"filterType": "listFilter"},
                                   headers=_get_authenticated_headers(phone_number, session_token, token_type))

    _ = _validate_response(update_response)


def check_token(phone_number: int, session_token: bytes, token_type: TokenType) -> None:
    ts = int(time.time())
    check_token_response = requests.get(urljoin(BASE_URL, f'user/check-token?ts={ts}&ts_diff=0'),
                                        headers=_get_authenticated_headers(phone_number, session_token, token_type))

    _ = _validate_response(check_token_response)


def _basic_headers() -> dict[str, str]:
    return {
        'User-Agent': ANDROID_USER_AGENT,
    }


def _get_authenticated_headers(phone_number: int, session_token: bytes, token_type: TokenType) -> dict[str, str]:
    return {
        **_basic_headers(),
        'X-Bt-Token': pylgate.generate_token(session_token, phone_number, token_type),
    }


def _validate_response(response: requests.Response) -> dict[str, Any]:
    response_data = response.json()
    if not response.ok or response_data['err'] or response_data['status'] != 'ok':
        raise RuntimeError(f"Step failed. full response: {response_data}")

    return response_data


if __name__ == "__main__":
    main()
