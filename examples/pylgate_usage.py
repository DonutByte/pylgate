# This program is dedicated to the public domain under the Creative Commons Attribution 3.0 Unported License.

"""
Example usage of the pylgate project

Note:
you must install pylgate via:
`pip install git+https://github.com/DonutByte/pylgate.git@main`

And install a http library, for this example we'll use requests
`pip install requests`
"""
from pylgate import generate_token
from pylgate.types import TokenType
import requests

SESSION_TOKEN = bytes.fromhex('<redacted>')  # The session token acquired via SMS or Device Linking
PHONE_NUMBER = 972501234567
TOKEN_TYPE = TokenType.SECONDARY

token = generate_token(SESSION_TOKEN, PHONE_NUMBER, TOKEN_TYPE)

ANDROID_USER_AGENT = 'okhttp/4.9.3'

response = requests.get(r'https://api1.pal-es.com/v1/bt/user/check-token',
                        headers={
                            'User-Agent': ANDROID_USER_AGENT,
                            'X-Bt-Token': token,
                        })

response_data = response.json()
if not response.ok or response_data['err'] or response_data['status'] != 'ok':
    print('Request failed')
    print(response_data)
    exit(1)

print('Response got:')
print(response_data)
