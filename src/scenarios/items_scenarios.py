from http import HTTPStatus

from src.api.api_manager import ApiManager
from src.data_models.errors import HTTPValidationErrorModel
from src.data_models.items import CreationItemModel, ItemModel, ItemsListModel, DeleteItemResponseModel, \
    ItemNotFoundModel
from src.utils.response_validator import validate_response


class ItemsScenarios:
    def __init__(self, api_manager: ApiManager):
        self.api_manager = api_manager

    def create_item(self, item_data: CreationItemModel, expected_status_code=HTTPStatus.OK):
        created_item_response = self.api_manager.items_api_client.create_item(
            item_data,
            expected_status_code=expected_status_code)
        created_item_model: ItemModel = validate_response(created_item_response, ItemModel)
        verify_creation_response = self.get_item_by_id(created_item_model.id)

        assert item_data.title == verify_creation_response.title, \
            (f'Created item title not equals to initial: '
             f'\nInitial: {item_data.title}'
             f'\nCreated: {verify_creation_response.title}')
        assert item_data.description == verify_creation_response.description, \
            (f'Created item title not equals to initial: '
             f'\nInitial: {item_data.description}'
             f'\nCreated: {verify_creation_response.description}')
        assert item_data.title == created_item_model.title, \
            (f'Initial title not equals to created one: '
             f'\nInitial: {item_data.title}\nGot: '
             f'{created_item_model.title}')
        assert item_data.description == created_item_model.description, \
            (f'Initial description not equals to created one: '
             f'\nInitial: {item_data.description}\nGot: '
             f'{created_item_model.description}')

        return created_item_model

    def create_item_negative(self, item_data: CreationItemModel, expected_status_code=422):
        created_item_response = self.api_manager.items_api_client.create_item(item_data,
                                                                              expected_status_code=expected_status_code)
        creation_error_model: HTTPValidationErrorModel = validate_response(
            created_item_response,
            HTTPValidationErrorModel)
        error_model = creation_error_model.detail[0]

        assert error_model.type == 'string_too_short', f'Unexpected error type: {error_model.type}'
        assert error_model.msg == 'String should have at least 1 character', \
            f'Unexpected error message: {error_model.msg}'
        assert error_model.loc == ['body', 'title'], \
            f'Unexpected error location: {error_model.loc}'
        assert error_model.ctx.min_length == 1, f'Unexpected ctx response: {error_model.ctx.min_length}'
        return creation_error_model

    def get_all_items(self, expected_status_code=HTTPStatus.OK):
        all_items_response = self.api_manager.items_api_client.get_items_list(expected_status_code=expected_status_code)
        all_items_model: ItemsListModel = validate_response(all_items_response, ItemsListModel)

        return all_items_model

    def get_item_by_id(self, item_id: int | str, expected_status_code=HTTPStatus.OK):
        item_response = self.api_manager.items_api_client.get_item_by_id(item_id,
                                                                         expected_status_code=expected_status_code)
        item_model: ItemModel = validate_response(item_response, ItemModel)

        assert item_id == item_model.id, \
            (f'Received item id not equals to sent one: '
             f'\nSent: {item_id}'
             f'\nGot: {item_model.id}')

        return item_model

    def verify_items_list_exists(self, items_to_verify_list: list[ItemModel]):
        all_existing_items_list = self.get_all_items().data

        for item in items_to_verify_list:
            assert item in all_existing_items_list

    def delete_item_by_id(self, item_id: int | str):
        delete_response = self.api_manager.items_api_client.delete_item(item_id)
        delete_response_model: DeleteItemResponseModel = validate_response(delete_response, DeleteItemResponseModel)

        verify_delete_response = self.api_manager.items_api_client.delete_item(item_id, expected_status_code=404)
        verify_delete_response_model: ItemNotFoundModel = validate_response(verify_delete_response, ItemNotFoundModel)

        assert delete_response_model.message == 'Item deleted successfully', \
            f'Unexpected message after item removal: {delete_response_model.message}'
        assert verify_delete_response_model.detail == 'Item not found', \
            f'Unexpected detail message on item removal verification: {verify_delete_response_model.detail}'

    def update_item(self, item_id: int | str, new_data_model: CreationItemModel):
        initial_item_data_model = self.get_item_by_id(item_id)

        updated_item_response = self.api_manager.items_api_client.update_item(item_id, new_data_model)
        updated_item_model: ItemModel = validate_response(updated_item_response, ItemModel)

        assert initial_item_data_model.title != updated_item_model.title, \
            (f'Item title did not change: '
             f'\nInitial: {initial_item_data_model.title}'
             f'\nNew: {updated_item_model.title}')
        assert initial_item_data_model.description != updated_item_model.description, \
            (f'Item description did not change: '
             f'\nInitial: {initial_item_data_model.description}'
             f'\nNew: {updated_item_model.description}')

        return updated_item_model

    def create_item_and_update(self, initial_data_model, new_data_model):
        created_item_model = self.create_item(initial_data_model)
        updated_item_model = self.update_item(created_item_model.id, new_data_model)

        return updated_item_model

    def create_item_and_delete(self, item_data: CreationItemModel):
        created_item_model = self.create_item(item_data)
        self.delete_item_by_id(created_item_model.id)
