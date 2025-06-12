from src.api.auth_api_client import AuthApi
from src.api.items_api_client import ItemsApiClient


class ApiManager:
    def __init__(self, session):
        self.session = session
        self.items_api_client = ItemsApiClient(session)
        self.auth_api_client = AuthApi(session)
