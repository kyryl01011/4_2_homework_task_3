import pytest
import requests

from custom_requester.custom_requester import CustomRequester
from src.api.api_manager import ApiManager
from src.api.auth_api import AuthApi
from src.api.items_scenarios import ItemsScenarios
from src.data_models.items import CreationItemModel
from src.enums.constant import AUTH_HEADERS, AUTH_DATA, API_HEADERS
from src.utils.data_generator import DataGenerator


@pytest.fixture(scope='session')
def session():
    session = requests.Session()
    session.headers.update(AUTH_HEADERS)
    yield session
    session.close()


@pytest.fixture(scope='session')
def authed_api_manager(session):
    api_manager = ApiManager(session)
    api_manager.auth_api.auth_current_session()
    return api_manager


@pytest.fixture(scope='session')
def items_scenarios(authed_api_manager):
    scenarios = ItemsScenarios(authed_api_manager)


@pytest.fixture
def item_data(auth_session):
    created_items = []

    def _create_item_data():
        random_data_model = CreationItemModel(
            title=DataGenerator.generate_random_word(),
            description=DataGenerator.generate_random_word()
        )
        created_items.append(random_data_model.title)
        return random_data_model

    yield _create_item_data

    # teardown
    items_list: list = auth_session.send_request('GET', f'/api/v1/items/').json().get('data', [])
    for item_title in created_items:
        for item in items_list:
            if item_title == item['title']:
                auth_session.send_request('DELETE', f'/api/v1/items/{item['id']}')
