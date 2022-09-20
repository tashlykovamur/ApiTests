from http import HTTPStatus

import pytest
from hamcrest import assert_that, equal_to, contains_string
from framework.client import HttpClient
import allure

from framework.helpers import parsed

client = HttpClient()
class TestGetCharacters:
    @allure.description('Получение всех существующих героев из базы под авторизованным пользователем')
    def test_get_all_characters(self, reset, get_exist_hero_name, auth):
        with allure.step('Достаем из базы информацию обо всех героях'):
            response = client.get_characters(auth=auth)

        with allure.step('Проверяем, что по запросу существующего героя приходит статус код 200'):
            assert_that(response.status_code, equal_to(HTTPStatus.OK))

    @allure.description('Получение существующего героя под авторизованным пользователем')
    def test_get_exist_character(self, reset, get_exist_hero_name, auth):
        with allure.step('Запрашиваем информацию о найденном в базе герое'):
            response = client.get_character(name=parsed(get_exist_hero_name), auth=auth)

        with allure.step('Проверяем, что по запросу существующего героя приходит статус код 200'):
            assert_that(response.status_code, equal_to(HTTPStatus.OK))

    @allure.description('Получение данных о героях под неавторизованным пользователем')
    def test_get_all_characters_wo_auth(self, reset):
        with allure.step('Запрашиваем данные о героях без ввода username и password'):
            response = client.get_characters()

        with allure.step('Проверяем, что в ответ приходит 401 статус код и сообщение об ошибке'):
            assert_that(response.status_code, equal_to(HTTPStatus.UNAUTHORIZED))
            assert_that(response.text, contains_string('You have to login with proper credentials'),
                        'При попытке получить данные без авторизации '
                        'должно приходить сообщение о необходимости авторизоваться')

    @allure.description('Получение данные о герое под неавторизованным пользователем')
    def test_get_character_wo_auth(self, reset, get_exist_hero_name):
        with allure.step('Запрашиваем данные о герое, не указывая username и password'):
            response = client.get_character(name=parsed(get_exist_hero_name))

        with allure.step('Проверяем,, что в ответ приходит 400 статус код и сообщение об ошибке'):
            assert_that(response.status_code, equal_to(HTTPStatus.UNAUTHORIZED))
            assert_that(response.text, contains_string('You have to login with proper credentials'),
                        'При попытке получить данные о герое без авторизации '
                        'должно приходить сообщение о необходимости залогиниться')

    @allure.description('Получение данные о герое без указания обязательного поля "name"')
    def test_get_character_wo_required_name(self, reset, auth):
        with allure.step('Запрашиваем данные о герое без обязательного поля "name"'):
            response = client.get_character(auth=auth)

        with allure.step('Проверяем, что в ответ приходит 400 статус код и сообщение об ошибке'):
            assert_that(response.status_code, equal_to(HTTPStatus.BAD_REQUEST))
            assert_that(response.text, contains_string('name parameter is required'),
                        'Должно приходить сообщение об обязательности заполнения поля "name"')

    @pytest.mark.parametrize(
        ('invalid_data', 'by_invalid_name'),
        [
            (None, 'без поля "name"'),
            ('', 'с пустым полем "name"'),
            (123, 'со значением не строкового типа int в поле "name"'),
            (True, 'со значением не строкового типа bool в поле "name"'),
            ('Pepega', ', которого нет в базе')
        ]
    )
    @allure.description('Получение данных о герое c некорректно заполненным полем "name"')
    def test_get_character_with_invalid_name(self, reset, auth, invalid_data, by_invalid_name):
        with allure.step(f'Запросить информацию о герое {by_invalid_name}'):
            response = client.get_character(name=invalid_data, auth=auth)

        with allure.step('Проверяем, что по запросу героя с невалидным именем приходит 400 статус код'):
            assert_that(response.status_code, equal_to(HTTPStatus.BAD_REQUEST))
