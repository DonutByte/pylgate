# This program is dedicated to the public domain under the Creative Commons Attribution 3.0 Unported License.

"""
This program generates a new session token as a Linked Device.

For detailed explanation on Device Linking, go to https://www.pal-es.com/tutorials

Note:
you must install `qrcode` and `requests` via
`pip install qrcode requests`
"""
import json
import uuid
import qrcode
import requests

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

unique_id = uuid.uuid4()
qr.add_data(f'{{"id": "{unique_id}"}}')
qr.make(fit=True)

print('Please open your palgate app, and scan this QR code:')
qr.print_ascii(invert=True)

ANDROID_USER_AGENT = 'okhttp/4.9.3'

response = requests.get(
    f'https://api1.pal-es.com/v1/bt/un/secondary/init/{unique_id}',
    headers={'User-Agent': ANDROID_USER_AGENT},
)

response_data = response.json()
if not response.ok or response_data['err'] or response_data['status'] != 'ok':
    print('Failed to login')
    print(response_data)
    exit(1)

data = {
    'id': int(response_data['user']['id']),
    'sessionToken': response_data['user']['token'],
}

print(f'Necessary values: {json.dumps(data, indent=4)}')

print('\nEverything:')
print(response_data)
