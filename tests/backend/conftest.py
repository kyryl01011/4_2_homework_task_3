import pytest
import requests

from custom_requester.custom_requester import CustomRequester
from enums.constant import AUTH_HEADERS, AUTH_DATA, BASE_URL, API_HEADERS
from utils.data_generator import DataGenerator


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
    requester.session.headers.update(API_HEADERS)
    requester.session.headers.update({'Authorization': 'Bearer ' + token})
    return requester

@pytest.fixture
def item_data(auth_session):
    created_items = []

    def _create_item_data():
        random_data = {
            'title': DataGenerator.generate_random_word(),
            'description': DataGenerator.generate_random_word()
        }
        created_items.append(random_data['title'])
        return random_data

    yield _create_item_data

    # teardown
    items_list: list = auth_session.send_request('GET', f'/api/v1/items/').json().get('data', [])
    for item_title in created_items:
        for item in items_list:
            if item_title == item['title']:
                auth_session.send_request('DELETE', f'/api/v1/items/{item['id']}')