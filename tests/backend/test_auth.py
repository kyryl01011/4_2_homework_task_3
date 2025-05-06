from utils.helpers import TEST_EMAIL


class TestAuth:

    def test_successful_get_current_user(self, auth_session):
        response = auth_session.send_request('GET', '/api/v1/users/me')
        current_user_data = response.json()
        assert current_user_data['email'] == TEST_EMAIL