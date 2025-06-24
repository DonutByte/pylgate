from typing import Any
from urllib.parse import urljoin

import httpx

from pylgate.types import TokenType


class PalgateAPI:
    _BASE_URL = 'https://api1.pal-es.com/v1/bt/'
    _ANDROID_USER_AGENT = 'okhttp/4.9.3'
    _DEFAULT_HEADERS = {
        'User-Agent': _ANDROID_USER_AGENT,
    }

    @staticmethod
    async def check_token(derived_token: str):
        return await PalgateAPI._do_get(f'user/check-token', PalgateAPI._get_authenticated_headers(derived_token))

    @staticmethod
    async def get_all_devices(derived_token: str):
        return await PalgateAPI._do_get('devices', PalgateAPI._get_authenticated_headers(derived_token))

    @staticmethod
    async def open_gate(derived_token: str, device_id: str):
        if ':' in device_id:
            normalized_device_id, output_num = device_id.split(':', maxsplit=1)
        else:
            normalized_device_id, output_num = device_id, 1

        return await PalgateAPI._do_get(f'device/{device_id}/open-gate?openBy=100&outputNum={output_num}',
                                        PalgateAPI._get_authenticated_headers(derived_token))

    @staticmethod
    async def start_device_linking(unique_id: str):
        return await PalgateAPI._do_get(f'un/secondary/init/{unique_id}', PalgateAPI._DEFAULT_HEADERS)

    @staticmethod
    async def link_device(derived_token: str, unique_id: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                urljoin(PalgateAPI._BASE_URL, f'secondary/init/{unique_id}'),
                json={
                    'secondary': str(TokenType.SECONDARY),  # FIXME this **OVERRIDES** secondary token!
                    'name': 'test',
                },
                headers=PalgateAPI._get_authenticated_headers(derived_token)
            )

        return PalgateAPI._validate_response(response)

    @staticmethod
    async def unlink_device(derived_token: str, token_type: TokenType):
        return await PalgateAPI._do_get(
            f'secondary/unlink?secondary={int(token_type)}',
            headers=PalgateAPI._get_authenticated_headers(derived_token)
        )

    @staticmethod
    async def _do_get(partial_url: str, headers: dict[str, str]):
        async with httpx.AsyncClient() as client:
            response = await client.get(urljoin(PalgateAPI._BASE_URL, partial_url), headers=headers)

        return PalgateAPI._validate_response(response)

    @staticmethod
    def _get_authenticated_headers(derived_token: str) -> dict[str, str]:
        return {
            **PalgateAPI._DEFAULT_HEADERS,
            'X-Bt-Token': derived_token,
        }

    @staticmethod
    def _validate_response(response: httpx.Response) -> dict[str, Any]:
        response_data = response.json()
        if response.is_error or response_data['err'] or response_data['status'] != 'ok':
            raise RuntimeError(f'Request failed. full response: {response_data}')

        return response_data
