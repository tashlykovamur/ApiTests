import json
import random

from framework.client import HttpClient
import pytest
from requests.auth import HTTPBasicAuth
from framework import config
import uuid


@pytest.fixture(autouse=True)
def reset(auth):
    HttpClient.reset_changes(url='http://rest.test.ivi.ru/v2/reset',
                             auth=auth)
    yield


@pytest.fixture()
def auth():
    return HTTPBasicAuth(config.username, config.password)


@pytest.fixture()
def fill_database(auth):
    for i in range(500):
        hero_name = str(uuid.uuid4())
        payload = {
            "name": hero_name,
            "weight": 104,
            "identity": "Publicly known"
        }
        response = HttpClient.create_character(
            url='/character',
            auth=auth,
            json=payload)

        if response.status_code == 400:
            break

    return response

@pytest.fixture()
def get_exist_hero_name(auth):
    response = HttpClient.get_characters(url='/characters', auth=auth)
    num = random.randint(0, 100)
    name = json.loads(response.text)['result'][num]['name']
    return name


