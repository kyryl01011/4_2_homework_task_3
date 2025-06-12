from src.custom_requester.custom_requester import CustomRequester
from src.enums.url_components import URLComponents


class AuthApi(CustomRequester):

    def auth_current_session(self):
        response = self.send_request('POST', '/api/v1/login/access-token', data=URLComponents.AUTH_DATA.value)
        token = response.json()['access_token']
        self.session.headers.update(URLComponents.API_HEADERS.value)
        self.session.headers.update({'Authorization': 'Bearer ' + token})
