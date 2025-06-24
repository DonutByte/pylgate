from dataclasses import dataclass

import pytest

from pylgate import generate_token
from pylgate.types import TokenType


def pytest_addoption(parser):
    parser.addoption('--session-token', action='store', required=True)
    parser.addoption('--phone-number', action='store', required=True, type=int)
    parser.addoption('--token-type', action='store', required=True, type=int)


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

    return SessionContext(bytes.fromhex(session_token), int(phone_number), TokenType(int(token_type)))


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
