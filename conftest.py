import json
import random
from http import HTTPStatus

import allure
from requests import Response

from framework.client import HttpClient
import pytest
from requests.auth import HTTPBasicAuth
from framework import config
import uuid


@pytest.fixture(autouse=True)
def reset(auth):
    client = HttpClient()
    client.reset_changes(auth)
    yield

@pytest.fixture()
def auth():
    return HTTPBasicAuth(config.username, config.password)


@pytest.fixture()
def fill_database() -> Response:
    with allure.step('Создаем 501 героя для переполнения базы'):
        client = HttpClient()
        for i in range(500):
            hero_name = str(uuid.uuid4())
            payload = {
                "name": hero_name,
                "weight": 104,
                "identity": "Publicly known"
            }
            response = client.create_character(json=payload)

            if response.status_code == HTTPStatus.BAD_REQUEST:
                break
        return response


@pytest.fixture()
def get_exist_hero_name(auth) -> str:
    with allure.step('Достаем из базы существующего героя по полю "name"'):
        client = HttpClient()
        response = client.get_characters(auth=auth)
        num = random.randint(0, 100)
        name = json.loads(response.text)['result'][num]['name']
        return name
