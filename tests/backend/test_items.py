

class TestItems:
    def __init__(self):
        self.endpoint = '/api/v1/items/'

    def test_delete_all_items(self, auth_session):
        items_list: list = auth_session.send_request('GET', f'/api/v1/items/').json().get('data', [])
        for item in items_list:
            auth_session.send_request('DELETE', f'/api/v1/items/{item['id']}')
        new_list = auth_session.send_request('GET', f'/api/v1/items/').json().get('data', [])
        assert new_list == []

    def test_successful_item_create(self, auth_session, item_data):
        generated_item_data = item_data()
        create_item_response = auth_session.send_request('POST', '/api/v1/items/', generated_item_data)
        response_dict = create_item_response.json()
        assert response_dict['title'] == generated_item_data['title'], f'Generated title: {generated_item_data['title']} not equals to created: {response_dict['title']}'
        assert response_dict['description'] == generated_item_data['description'], f'Generated desc: {generated_item_data['description']} not equals to created: {response_dict['description']}'
        return response_dict['id']

    def test_negative_item_create(self, auth_session, item_data):
        generated_item_data = item_data()
        create_item_response = auth_session.send_request('POST', '/api/v1/items/', generated_item_data, expected_status_code=422)
        response_dict = create_item_response.json()
        assert type(response_dict['detail'][0]['loc'][0]) is str

    def test_pagination_with_twenty_items_creation(self, auth_session, item_data):
        created_items_ids = []
        for item in range(20):
            created_item_id = self.test_successful_item_create(auth_session, item_data)
            created_items_ids.append(created_item_id)
        return created_items_ids

    def test_get_all_items_list(self, auth_session, item_data):
        items_ids_list = self.test_pagination_with_twenty_items_creation(auth_session, item_data)
        all_items_response = auth_session.send_request('GET', f'/api/v1/items/')
        all_items_data = all_items_response.json().get('data', [])
        all_items_count = all_items_response.json()['count']
        assert all_items_response.json()['count'], f'"count" key cant be found in response: {all_items_response.json()}'
        for item in all_items_data:
            assert 'title' in item.keys(), f'No key with name "title" in response data dict {item}'
            assert 'description' in item.keys(), f'No key with name "description" in response data dict {item}'
            assert 'id' in item.keys(), f'No key with name "id" in response data dict {item}'
            assert 'owner_id' in item.keys(), f'No key with name "owner_id" in response data dict {item}'
        assert type(all_items_count) is int, ''

    def test_full_update_item_by_id(self, auth_session, item_data):
        initial_item_id = self.test_successful_item_create(auth_session, item_data)
        fresh_item_data = item_data()
        update_response = auth_session.send_request('PUT', f'')