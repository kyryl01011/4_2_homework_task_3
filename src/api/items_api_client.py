from http import HTTPStatus

from src.custom_requester.custom_requester import CustomRequester


class ItemsApiClient(CustomRequester):
    _BASE_ENDPOINT = '/api/v1/items/'

    def get_items_list(self, expected_status_code=HTTPStatus.OK):
        response = self.send_request('GET', self._BASE_ENDPOINT, expected_status_code=expected_status_code)
        return response

    def create_item(self, item_data, expected_status_code=HTTPStatus.OK):
        response = self.send_request('POST', self._BASE_ENDPOINT, json=item_data,
                                     expected_status_code=expected_status_code)
        return response

    def get_item_by_id(self, item_id, expected_status_code=HTTPStatus.OK):
        response = self.send_request('GET', f'{self._BASE_ENDPOINT}{item_id}',
                                     expected_status_code=expected_status_code)
        return response

    def update_item(self, item_id, new_data=None, expected_status_code=HTTPStatus.OK):
        response = self.send_request('PUT', f'{self._BASE_ENDPOINT}{item_id}', json=new_data,
                                     expected_status_code=expected_status_code)
        return response

    def delete_item(self, item_id, expected_status_code=HTTPStatus.OK):
        response = self.send_request('DELETE', f'{self._BASE_ENDPOINT}{item_id}',
                                     expected_status_code=expected_status_code)
        return response
