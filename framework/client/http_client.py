import requests
from requests import Response

class HttpClient:
    def __init__(self):
        self.TEST_URL = 'http://rest.test.ivi.ru/v2'
        self.CHARACTERS_PATH = '/characters'
        self.CHARACTER_PATH = '/character'

    def get_characters(self, params: dict = None, auth=None,) -> Response:
        return requests.get(self.TEST_URL+self.CHARACTERS_PATH, params, auth=auth)

    def get_character(self, name: str = None, auth=None) -> Response:
        return requests.get(self.TEST_URL+self.CHARACTER_PATH, params={'name': name}, auth=auth)

    def create_character(self, json: dict = None, auth=None,) -> Response:
        return requests.post(self.TEST_URL, json=json, auth=auth)

    def edit_character(self, json: dict = None, auth=None) -> Response:
        return requests.put(self.TEST_URL, json=json, auth=auth)

    def delete_character(self, name: str = None, auth=None) -> Response:
        return requests.delete(self.TEST_URL, params={'name': name}, auth=auth)

    def reset_changes(self, auth) -> Response:
        return requests.post(self.TEST_URL+'/reset', auth=auth)
