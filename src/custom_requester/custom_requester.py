from http import HTTPStatus

from pydantic import BaseModel
from requests import Session

from src.enums.url_components import URLComponents


class CustomRequester:
    def __init__(self, session: Session):
        self.session = session

    def send_request(self, method, endpoint, json: BaseModel | None = None, data=None,
                     expected_status_code=HTTPStatus.OK):
        url = URLComponents.BASE_URL.value + URLComponents.BASE_API_ENDPOINT.value + endpoint
        if json:
            json = json.model_dump()

        response = self.session.request(method, url, json=json, data=data)

        assert expected_status_code == response.status_code, \
            f'Unexpected status code: expected {expected_status_code}, got {response.status_code}'

        return response
