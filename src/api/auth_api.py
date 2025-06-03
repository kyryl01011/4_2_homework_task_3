from src.custom_requester.custom_requester import CustomRequester
from src.utils.consts import AUTH_DATA, API_HEADERS


class AuthApi(CustomRequester):

    def auth_current_session(self):
        response = self.send_request('POST', '/api/v1/login/access-token', data=AUTH_DATA)
        token = response.json()['access_token']
        self.session.headers.update(API_HEADERS)
        self.session.headers.update({'Authorization': 'Bearer ' + token})
