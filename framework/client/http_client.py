import requests
from requests import Response

from constants import TEST_URL


class HttpClient:

    @staticmethod
    def get_characters(url: str, json=None, auth=None) -> Response:
        return HttpClient._send(url, json, auth, 'GET')

    @staticmethod
    def get_character(url: str, params: dict = None, auth=None) -> Response:
        return HttpClient._send(url, params, auth, 'GET')

    @staticmethod
    def create_character(url: str, json: dict = None, auth=None) -> Response:
        return HttpClient._send(url, json, auth, 'POST')

    @staticmethod
    def edit_character(url: str, json: dict = None, auth=None) -> Response:
        return HttpClient._send(url, json, auth, 'PUT')

    @staticmethod
    def delete_character(url: str, params: dict = None, auth=None) -> Response:
        return HttpClient._send(url, params, auth, 'DELETE')

    @staticmethod
    def reset_changes(url: str, auth=None) -> Response:
        return requests.post(url, auth=auth)

    @staticmethod
    def _send(path: str = None, json: dict = None, auth=None, method: str = None) -> Response:
        url = f"{TEST_URL}{path}"

        if method == 'GET':
            response = requests.get(url, json=json, auth=auth)
        elif method == 'POST':
            response = requests.post(url, json=json, auth=auth)
        elif method == 'PUT':
            response = requests.put(url, json=json, auth=auth)
        elif method == 'DELETE':
            response = requests.delete(url, json=json, auth=auth)
        else:
            raise Exception(f"Получен некорректный HTTP метод'{method}'")

        return response
