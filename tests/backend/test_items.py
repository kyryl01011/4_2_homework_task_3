class TestItems:

    def test_delete_all_items(self, auth_session):
        items_list: list = auth_session.send_request('GET', '/api/v1/items/').json().get('data', [])
        for item in items_list:
            auth_session.send_request('DELETE', f'/api/v1/items/{item['id']}')
        new_list = auth_session.send_request('GET', '/api/v1/items/').json().get('data', [])
        assert new_list == [], f'List is not empty: {new_list}'

    def test_successful_item_create(self, auth_session, item_data):
        generated_item_data = item_data()
        create_item_response = auth_session.send_request('POST', '/api/v1/items/', generated_item_data)
        response_dict = create_item_response.json()
        assert response_dict['title'] == generated_item_data['title'], f'Generated title: {generated_item_data['title']} not equals to created: {response_dict['title']}'
        assert response_dict['description'] == generated_item_data['description'], f'Generated desc: {generated_item_data['description']} not equals to created: {response_dict['description']}'
        return response_dict

    def test_negative_item_create(self, auth_session, item_data):
        generated_item_data = item_data()
        create_item_response = auth_session.send_request('POST', '/api/v1/items/', {'title': ''}, expected_status_code=422)
        err_message_response = create_item_response.json()['detail'][0]
        print(err_message_response)
        assert err_message_response['type'] == 'string_too_short', f'Unexpected error type: {err_message_response['type']}'
        assert err_message_response['msg'] == 'String should have at least 1 character', f'Unexpected error message: {err_message_response['msg']}'
        assert err_message_response['input'] == '', f'Unexpected input: {err_message_response['input']}'
        assert err_message_response['loc'] == ['body', 'title'], f'Unexpected error location: {err_message_response['loc']}'

    def test_pagination_with_twenty_items_creation(self, auth_session, item_data):
        created_items_ids = []
        for item in range(20):
            created_item_id = self.test_successful_item_create(auth_session, item_data)['id']
            created_items_ids.append(created_item_id)
        all_items_response = auth_session.send_request('GET', '/api/v1/items/')
        all_items_response_data = all_items_response.json().get('data', [])
        all_items_response_ids = [item['id'] for item in all_items_response_data]
        for item_id in created_items_ids:
            assert item_id in all_items_response_ids, f'No ID of created item in existing items data: {item_id}'
        return created_items_ids

    def test_get_all_items_list(self, auth_session, item_data):
        items_ids_list = self.test_pagination_with_twenty_items_creation(auth_session, item_data)
        all_items_response = auth_session.send_request('GET', '/api/v1/items/')
        all_items_data = all_items_response.json().get('data', [])
        all_items_count = all_items_response.json()['count']
        assert all_items_response.json()['count'], f'"count" key cant be found in response: {all_items_response.json()}'
        for item in all_items_data:
            assert 'title' in item.keys(), f'No key with name "title" in response data dict {item}'
            assert 'description' in item.keys(), f'No key with name "description" in response data dict {item}'
            assert 'id' in item.keys(), f'No key with name "id" in response data dict {item}'
            assert 'owner_id' in item.keys(), f'No key with name "owner_id" in response data dict {item}'
        assert type(all_items_count) is int, f'Unexpected count response type: {type(all_items_count)}'

    def test_full_update_item_by_id(self, auth_session, item_data):
        initial_item = self.test_successful_item_create(auth_session, item_data)
        fresh_item_data = item_data()
        update_response = auth_session.send_request('PUT', f'/api/v1/items/{initial_item['id']}', json=fresh_item_data).json()
        for key in update_response.keys(): # чисто для практики циклов, вместо 2 ассертов
            if key not in ('id', 'owner_id'):
                assert initial_item[key] != update_response[key], f'Field {key} did not change: initial {initial_item[key]}, new one {update_response[key]}'

    def test_delete_item_by_id(self, auth_session, item_data):
        initial_item_id = self.test_successful_item_create(auth_session, item_data)['id']
        delete_response = auth_session.send_request('DELETE', f'/api/v1/items/{initial_item_id}')
        assert delete_response.json()['message'] == 'Item deleted successfully', f'Delete response has no message confirmation: {delete_response.json()['message']}'
        addition_check_response = auth_session.send_request('GET', f'/api/v1/items/{initial_item_id}', expected_status_code=404)
        assert addition_check_response.json()['detail'] == 'Item not found', f'Delete response has no message confirmation: {addition_check_response.json()['detail']}'