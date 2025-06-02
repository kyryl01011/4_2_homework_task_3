import pytest
import requests

from src.api.api_manager import ApiManager
from src.scenarios.items_scenarios import ItemsScenarios
from src.data_models.items import CreationItemModel, ItemModel
from src.consts import AUTH_HEADERS
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
    return scenarios


@pytest.fixture
def item_data(items_scenarios):
    def _create_item_data():
        random_data_model = CreationItemModel(
            title=DataGenerator.generate_random_word(),
            description=DataGenerator.generate_random_word()
        )
        return random_data_model

    yield _create_item_data

    # teardown
    all_existing_items = items_scenarios.get_all_items().data
    all_existing_ids = (item.id for item in all_existing_items)

    for item_id in ItemModel.created_items_ids:
        if item_id in all_existing_ids:
            items_scenarios.delete_item_by_id(item_id)
