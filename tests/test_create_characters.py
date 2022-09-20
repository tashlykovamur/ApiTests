import pytest
from hamcrest import assert_that, equal_to, contains_string
from framework.client import HttpClient
import allure
from http import HTTPStatus
from framework.helpers import parsed

client = HttpClient()
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
        with allure.step('Создаем нового героя со значением типа "string" в поле "name"'):
            data = {
                "name": hero_name,
                "weight": 104,
                "identity": "Publicly known"
            }
            response = client.create_character(json=data, auth=auth)

        with allure.step('Проверяем, что по запросу приходит 200 статус код'):
            assert_that(response.status_code, equal_to(HTTPStatus.OK))

        with allure.step(f'Проверяем, что герой с именем "{hero_name}" появился в базе'):
            response = client.get_character(name=parsed(hero_name), auth=auth)
            assert_that(response.status_code, equal_to(HTTPStatus.OK))

    @allure.description('Создание героя под неавторизованным пользователем')
    def test_create_character_wo_auth(self, reset, auth):
        with allure.step('Создаем нового героя, не указывая username и password'):
            data = {
                "name": 'Pugster',
                "weight": 104,
                "identity": "Publicly known"
            }
            response = client.create_character(json=data)

        with allure.step('Проверяем, что нельзя создать нового героя'):
            assert_that(response.status_code, equal_to(HTTPStatus.UNAUTHORIZED))

    @allure.description('Создание героя с именем, которое уже существует в базе')
    def test_create_duplicate_character(self, reset, auth, get_exist_hero_name):
        with allure.step('Создаем героя с существующем именем в базе'):
            data = {
                "name": get_exist_hero_name,
                "weight": 104,
                "identity": "Publicly known"
            }
            response = client.create_character(json=data, auth=auth)

        with allure.step('Проверяем, что нельзя создать дубликат героя'):
            assert_that(response.status_code, equal_to(HTTPStatus.BAD_REQUEST))
            assert_that(response.text, contains_string(f'{get_exist_hero_name} is already exists'),
                        'В ответе должно быть сообщение, что такой герой уже существует')

    @pytest.mark.parametrize(
        ('invalid_data', 'by_invalid_name'),
        [
            (None, 'без поля "name"'),
            ("", 'с пустым полем "name"'),
            (123, 'со значением типа int в поле "name"'),
            (True, 'со значением типа bool в поле "name"')
        ]
    )
    @allure.description('Создание героя с некорректно заполненным полем "name"')
    def test_create_character_with_invalid_name(self, reset, invalid_data, by_invalid_name, auth):
        with allure.step(f'Создаем нового героя {by_invalid_name}'):
            data = {
                "name": invalid_data,
                "weight": 104,
                "identity": "Publicly known"
            }
            response = client.create_character(json=data, auth=auth)

        with allure.step('Проверяем, что при попытке создания героя с невалидным именем приходит 400 статус код'):
            assert_that(response.status_code, equal_to(HTTPStatus.BAD_REQUEST))

    @allure.description('Заполнение базы до максимально возможного количества героев (>500)')
    def test_create_too_many_characters(self, reset, auth, fill_database):
        with allure.step('Проверяем, что при переполнении базы приходит 400 статус код и сообщение об ошибке'):
            assert_that(fill_database.status_code, equal_to(HTTPStatus.BAD_REQUEST),
                        'При переполнении базы нельзя добавлять новые записи')
            assert_that(fill_database.text, contains_string('Collection can\'t contain more than 500 items'),
                        'При превышении вместимости базы должно приходить сообщение о невозможности хранения более 500 '
                        'героев')
