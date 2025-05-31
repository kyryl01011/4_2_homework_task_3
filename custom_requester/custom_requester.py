from pydantic import BaseModel
from requests import Session

from src.enums.constant import BASE_URL


class CustomRequester:
    def __init__(self, session: Session):
        self._base_url = BASE_URL
        self.session = session

    def get_url(self, endpoint):
        return self._base_url + endpoint

    def send_request(self, method, endpoint, json: BaseModel | None, data=None, expected_status_code=200):
        response = self.session.request(method, self.get_url(endpoint), json=json.model_dump(), data=data)

        print(f'''<><><><><>
    ---REQUEST---
    {response.request.method}
    {response.request.url}
    {response.request.body}
    ---RESPONSE---
    {response.status_code}
    {response.text}
<><><><><>''')

        assert expected_status_code == response.status_code, \
            f'Unexpected status code: expected {expected_status_code}, got {response.status_code}'

        return response
