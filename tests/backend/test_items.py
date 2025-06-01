import pytest

from src.api.items_scenarios import ItemsScenarios
from src.data_models.items import ItemModel
from tests.backend.conftest import items_scenarios


class TestItems:

    def test_successful_item_create(self, items_scenarios: ItemsScenarios, item_data):
        test_item_data = item_data()

        items_scenarios.create_item(test_item_data)

    def test_negative_item_create(self, items_scenarios: ItemsScenarios, item_data):
        test_item_data = item_data()
        test_item_data.title = ''
        items_scenarios.create_item_negative(test_item_data)

    def test_pagination_with_twenty_items_creation(self, items_scenarios: ItemsScenarios, item_data):
        created_items_list = []
        for item in range(20):
            test_data = item_data()
            created_item_response: ItemModel = items_scenarios.create_item(test_data)
            created_items_list.append(created_item_response)

        items_scenarios.verify_items_list_exists(created_items_list)

    def test_get_all_items_list(self, items_scenarios: ItemsScenarios):
        items_scenarios.get_all_items()

    def test_full_update_item_by_id(self, items_scenarios: ItemsScenarios, item_data):
        initial_model = item_data()
        new_model = item_data()

        items_scenarios.create_item_and_update(initial_model, new_model)

    def test_delete_item_by_id(self, items_scenarios: ItemsScenarios, item_data):
        test_data = item_data()

        items_scenarios.create_item_and_delete(test_data)
