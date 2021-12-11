import pytest
from hamcrest import assert_that, equal_to, contains_string
from framework.client import HttpClient
import allure
from http import HTTPStatus
from constants import CHARACTER_PATH
from framework.helpers import parsed


class TestCreateCharacters:
    @pytest.mark.parametrize('hero_name',
                             [
                                 'Black Widow',  # запрос, состоящий из 2х и более слов
                                 'Batman',  # запрос, состоящий из 1 слова
                                 'A'  # проверка минимально возможной границы
                             ]
                             )
    @allure.description('Создание героя под авторизованным пользователем с заполненным обязательным полем "name"')
    def test_create_new_character(self, reset, hero_name, auth):
        with allure.step('Создать нового героя со значением типа "string" в поле "name"'):
            payload = {
                "name": hero_name,
                "weight": 104,
                "identity": "Publicly known"
            }
            response = HttpClient.create_character(
                url=CHARACTER_PATH,
                auth=auth,
                json=payload
            )

        with allure.step('Проверить, что работает создание нового героя'):
            assert_that(response.status_code, equal_to(HTTPStatus.OK),
                        'При корректно заполненном поле "name" герой должен создаваться ')

        with allure.step(f'Проверить с помощью вызова /GET, что герой с именем \"{hero_name}\" появился в базе'):
            response = HttpClient.get_character(
                url=f'{CHARACTER_PATH}?name={parsed(hero_name)}',
                auth=auth)
            assert_that(response.status_code, equal_to(HTTPStatus.OK),
                        'Созданный герой с корректно заполненным полем "name" должен присутствовать в базе')

    @allure.description('Создание героя под неавторизованным пользователем')
    def test_create_character_wo_auth(self, reset):
        with allure.step('Создать нового героя, не указывая username и password'):
            payload = {
                "name": 'Pugster',
                "weight": 104,
                "identity": "Publicly known"
            }
            response = HttpClient.create_character(
                url=CHARACTER_PATH,
                json=payload
            )

        with allure.step('Проверить, что нельзя создать нового героя'):
            assert_that(response.status_code, equal_to(HTTPStatus.UNAUTHORIZED),
                        'Нельзя создать героя под неавторизованным пользователем')

    @allure.description('Создание героя с именем, которое уже существует в базе')
    def test_create_duplicate_character(self, reset, auth, get_exist_hero_name):
        with allure.step('Создать героя с существующем именем в базе'):
            payload = {
                "name": get_exist_hero_name,
                "weight": 104,
                "identity": "Publicly known"
            }
            response = HttpClient.create_character(
                url=CHARACTER_PATH,
                auth=auth,
                json=payload
            )

        with allure.step('Проверить, что нельзя создать дубликат героя'):
            assert_that(response.status_code, equal_to(HTTPStatus.BAD_REQUEST),
                        'Нельзя создать двух героев с одинаковым именем')
            assert_that(response.text, contains_string(f'{get_exist_hero_name} is already exists'),
                        'Должно приходить сообщение о том, что такой герой уже существует')

    @pytest.mark.parametrize(
        ('invalid_data', 'by_invalid_name'),
        [
            (None, 'cо значением null в поле "name"'),
            ("", 'с незаполненным полем "name"'),
            (123, 'со значением не строкового типа int в поле "name"'),
            (True, 'со значением не строкового типа bool в поле "name"')
        ]
    )
    @allure.description('Создание героя с некорректно заполненным полем "name"')
    def test_create_character_with_invalid_name(self, reset, invalid_data, by_invalid_name, auth):
        with allure.step(f'Создать нового героя {by_invalid_name}'):
            payload = {
                "name": invalid_data,
                "weight": 104,
                "identity": "Publicly known"
            }
            response = HttpClient.create_character(
                url=CHARACTER_PATH,
                auth=auth,
                json=payload
            )
        with allure.step('Проверить, что нельзя создать нового героя'):
            assert_that(response.status_code, equal_to(HTTPStatus.BAD_REQUEST),
                        f'Герой не должен создаваться {by_invalid_name}')

    @allure.description('Создание героя без обязательного поля "name"')
    def test_create_character_wo_required_name(self, reset, auth):
        with allure.step('Создать нового героя без обязательного поля "name"'):
            payload = {
                "weight": 104,
                "identity": "Publicly known"
            }
            response = HttpClient.create_character(
                url=CHARACTER_PATH,
                auth=auth,
                json=payload
            )

        with allure.step('Проверить, что не работает создание нового героя'):
            assert_that(response.status_code, equal_to(HTTPStatus.BAD_REQUEST),
                        'Нельзя создать героя без обязательного поля "name"')
            assert_that(response.text, contains_string('Missing data for required field'),
                        'Должно приходить сообщение об обязательности заполнения поля')

    @allure.description('Заполнение базы до максимально возможного количества героев (>500)')
    def test_create_too_many_characters(self, reset, auth, fill_database):
        with allure.step('Создать 501-го героя для переполнения базы'):
            response = fill_database

        with allure.step('Проверить, что при переполнении базы приходит ошибка'):
            assert_that(response.status_code, equal_to(HTTPStatus.BAD_REQUEST),
                        'При переполнении базы нельзя добавлять новые записи')
            assert_that(response.text, contains_string('Collection can\'t contain more than 500 items'),
                        'При превышении вместимости базы должно приходить сообщение о невозможности хранения более 500 '
                        'элементов')
