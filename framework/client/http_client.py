import json

import requests
from requests import post


class HttpClient:

    @staticmethod
    def get_characters(url: str, json: dict = None, auth=None):
        return HttpClient._send(url, json, auth, 'GET')

    @staticmethod
    def get_character(url: str, json: dict = None, auth=None):
        return HttpClient._send(url, json, auth, 'GET')

    @staticmethod
    def create_character(url: str, json: dict = None, auth=None):
        return HttpClient._send(url, json, auth, 'POST')

    @staticmethod
    def edit_character(url: str, json: dict = None, auth=None):
        return HttpClient._send(url, json, auth, 'PUT')

    @staticmethod
    def delete_character(url: str, params: dict = None, auth=None):
        return HttpClient._send(url, params, auth, 'DELETE')

    @staticmethod
    def reset_changes(url: str, auth=None):
        return post(url, auth=auth)

    @staticmethod
    def _send(uri: str = None, json: dict = None, auth=None, method: str = None):
        url = f"http://rest.test.ivi.ru/v2{uri}"

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
