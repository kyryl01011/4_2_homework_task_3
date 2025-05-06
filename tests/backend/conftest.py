import pytest
import requests

from custom_requester.custom_requester import CustomRequester
from enums.constant import AUTH_HEADERS, AUTH_DATA, BASE_URL


@pytest.fixture(scope='session')
def session():
    session = requests.Session()
    session.headers.update(AUTH_HEADERS)
    yield session
    session.close()

@pytest.fixture(scope='session')
def auth_session(session):
    requester = CustomRequester(session)
    response = requester.send_request('POST', '/api/v1/login/access-token', data=AUTH_DATA)
    token = response.json()['access_token']
    requester.session.headers.update({'Authorization': 'Bearer ' + token, "Content-Type": "application/json"})
    return requester