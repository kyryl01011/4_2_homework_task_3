from http import HTTPStatus

from pydantic import BaseModel
from requests import Session

from src.consts import BASE_URL


class CustomRequester:
    def __init__(self, session: Session):
        self._base_url = BASE_URL
        self.session = session

    def get_url(self, endpoint):
        return self._base_url + endpoint

    def send_request(self, method, endpoint, json: BaseModel | None = None, data=None,
                     expected_status_code=HTTPStatus.OK):
        if json:
            json = json.model_dump()

        response = self.session.request(method, self.get_url(endpoint), json=json, data=data)

        assert expected_status_code == response.status_code, \
            f'Unexpected status code: expected {expected_status_code}, got {response.status_code}'

        return response
