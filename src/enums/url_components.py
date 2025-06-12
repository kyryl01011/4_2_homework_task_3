from src.utils.helpers import TEST_EMAIL, TEST_PASS
from enum import Enum


class URLComponents(Enum):
    BASE_URL = "https://api.pomidor-stage.ru"

    BASE_API_ENDPOINT = "/api/v1/"

    AUTH_HEADERS = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }

    API_HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    AUTH_DATA = {
        "username": TEST_EMAIL,
        "password": TEST_PASS,
        "scope": "",
        "client_id": "",
        "client_secret": ""
    }
