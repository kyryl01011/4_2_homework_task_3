from typing import Type

from src.api.api_manager import ApiManager
from src.data_models.items import CreationItemModel, ItemModel, ItemsListModel
from src.utils.validate_response import validate_response


class ItemsScenarios:
    def __init__(self, api_manager: ApiManager):
        self.api_manager = api_manager

    def create_item(self, item_data: CreationItemModel, expected_status_code=None):
        created_item_response = self.api_manager.items_api_client.create_item(item_data,
                                                                              expected_status_code=expected_status_code)
        created_item_model: ItemModel = validate_response(created_item_response, ItemModel)

        assert item_data.title == created_item_model.title, \
            (f'Initial title not equals to created one: '
             f'\nInitial: {item_data.title}\nGot: '
             f'{created_item_model.title}')
        assert item_data.description == created_item_model.description, \
            (f'Initial description not equals to created one: '
             f'\nInitial: {item_data.description}\nGot: '
             f'{created_item_model.description}')

        return created_item_model

    def get_all_items(self, expected_status_code=None):
        all_items_response = self.api_manager.items_api_client.get_items_list(expected_status_code=expected_status_code)
        all_items_model: ItemsListModel = validate_response(all_items_response, ItemsListModel)

        return all_items_model

    def get_item_by_id(self, item_id, expected_status_code=None):
        item_response = self.api_manager.items_api_client.get_item_by_id(item_id,
                                                                         expected_status_code=expected_status_code)
        item_model: ItemModel = validate_response(item_response, ItemModel)

        assert item_id == item_model.id, \
            (f'Received item id not equals to sent one: '
             f'\nSent: {item_id}'
             f'\nGot: {item_model.id}')

        return item_model
