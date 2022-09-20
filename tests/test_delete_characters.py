from http import HTTPStatus

import pytest
from hamcrest import assert_that, equal_to, contains_string
from framework.client import HttpClient
import allure

from constants import CHARACTER_PATH
from framework.helpers import parsed

client = HttpClient()
class TestDeleteCharacters:

    @allure.description('Удаление существующего героя под авторизованным пользователем')
    def test_delete_exist_character(self, reset, get_exist_hero_name, auth):
        with allure.step('Отправляем запрос на удаление найденного героя будучи авторизованным'):
            response = client.delete_character(name=parsed(get_exist_hero_name), auth=auth)

        with allure.step('Проверяем, что запрос с удалением вернул статус код 200'):
            assert_that(response.status_code, equal_to(HTTPStatus.OK))

        with allure.step('Проверяем, что удаленного героя нет в базе'):
            response_after_delete = client.get_character(name=parsed(get_exist_hero_name), auth=auth)
            assert_that(response_after_delete.status_code, equal_to(HTTPStatus.BAD_REQUEST))

    @allure.description('Удаление героя под неавторизованным пользователем')
    def test_delete_character_wo_auth(self, reset, get_exist_hero_name):
        with allure.step('Отправляем запрос на удаление героя без указания username и password'):
            response = client.delete_character(name=parsed(get_exist_hero_name))

        with allure.step('Проверяем, что в ответ приходит статус код 401 и сообщение об ошибке'):
            assert_that(response.status_code, equal_to(HTTPStatus.UNAUTHORIZED))
            assert_that(response.text, contains_string('You have to login with proper credentials'),
                        'При попытке удалить героя без авторизации '
                        'должно приходить сообщение о необходимости залогиниться')

    @pytest.mark.parametrize(
        ('invalid_data', 'by_invalid_name'),
        [
            ('', 'с пустым полем "name"'),
            (123, 'со значением не строкового типа int в поле "name"'),
            (True, 'со значением не строкового типа bool в поле "name"'),
            ('Pepega', ', которого нет в базе')
        ]
    )
    @allure.description('Удаление героя c некорректно заполненным полем "name"')
    def test_delete_character_with_invalid_name(self, reset, auth, invalid_data, by_invalid_name):
        with allure.step(f'Отправляем запрос на удаление героя {by_invalid_name}'):
            response = client.delete_character(name=invalid_data, auth=auth)

        with allure.step('Проверяем, что в ответ приходит статус код 400'):
            assert_that(response.status_code, equal_to(HTTPStatus.BAD_REQUEST))

    @allure.description('Удаление героя без обязательного поля "name"')
    def test_delete_character_wo_required_name(self, reset, auth):
        with allure.step('Отправляем запрос на удаление героя без обязательного поля "name"'):
            response = client.delete_character(auth=auth)

        with allure.step('Проверяем, что в ответ приходит 400 статус код и сообщение об ошибке'):
            assert_that(response.status_code, equal_to(HTTPStatus.BAD_REQUEST))
            assert_that(response.text, contains_string('name parameter is required'),
                        f'Должно приходить сообщение об обязательности заполнения поля')
