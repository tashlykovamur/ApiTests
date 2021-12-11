import json
import random
from http import HTTPStatus
from requests import Response

from framework.client import HttpClient
import pytest
from requests.auth import HTTPBasicAuth
from framework import config
import uuid

from constants import TEST_URL, RESET_PATH, CHARACTER_PATH, CHARACTERS_PATH


@pytest.fixture(autouse=True)
def reset(auth):
    HttpClient.reset_changes(url=TEST_URL + RESET_PATH,
                             auth=auth)
    yield


@pytest.fixture()
def auth():
    return HTTPBasicAuth(config.username, config.password)


@pytest.fixture()
def fill_database(auth) -> Response:
    for i in range(500):
        hero_name = str(uuid.uuid4())
        payload = {
            "name": hero_name,
            "weight": 104,
            "identity": "Publicly known"
        }
        response = HttpClient.create_character(
            url=CHARACTER_PATH,
            auth=auth,
            json=payload)

        if response.status_code == HTTPStatus.BAD_REQUEST:
            break

    return response


@pytest.fixture()
def get_exist_hero_name(auth) -> str:
    response = HttpClient.get_characters(url=CHARACTERS_PATH, auth=auth)
    num = random.randint(0, 100)
    name = json.loads(response.text)['result'][num]['name']
    return name
