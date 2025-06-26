"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from dataclasses import dataclass

import pytest

from pylgate import generate_token
from pylgate.types import TokenType


def pytest_addoption(parser):
    parser.addoption('--session-token', action='store', required=True)
    parser.addoption('--phone-number', action='store', required=True, type=int)
    parser.addoption('--token-type', action='store', required=True, type=int, choices=TokenType.values())


@dataclass
class SessionContext:
    session_token: bytes
    phone_number: int
    token_type: TokenType


@pytest.fixture(scope='module')
def session_context(request) -> SessionContext:
    session_token = request.config.getoption('--session-token')
    phone_number = request.config.getoption('--phone-number')
    token_type = request.config.getoption('--token-type')

    return SessionContext(bytes.fromhex(session_token), phone_number, TokenType(token_type))


@pytest.fixture(scope='module')
def derived_token_generator(session_context):
    """
    Helper function to get a derived token lazily
    Returns:
        Callback which when called returns a newly generated derived token
    Notes:
        derived tokens are time-sensitive, call function right before necessary
    """

    def wrapper():
        return generate_token(session_context.session_token, session_context.phone_number, session_context.token_type)

    return wrapper
