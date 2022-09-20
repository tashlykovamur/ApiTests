import uuid
from http import HTTPStatus

import pytest
from hamcrest import assert_that, equal_to, contains_string
from framework.client import HttpClient
import allure

from constants import CHARACTER_PATH

client = HttpClient()


class TestUpdateCharacters:
    changed_data = str(uuid.uuid4())

    @allure.description('Редактирование существующего героя под авторизованным пользователем')
    def test_edit_exist_character(self, reset, get_exist_hero_name, auth):
        with allure.step('Отправляем запрос на изменение найденного героя будучи авторизованным'):
            data = {
                "name": get_exist_hero_name,
                "weight": 104,
                "identity": self.changed_data
            }
            response = client.edit_character(auth=auth, json=data)

        with allure.step('Проверяем, что в ответе статус код 200'):
            assert_that(response.status_code, equal_to(HTTPStatus.OK))

        with allure.step('Проверяем, что герой лежит в базе с обновленными данными'):
            response_after_edit = client.get_character(name=get_exist_hero_name,
                                                       auth=auth)
            assert_that(response_after_edit.text, contains_string(self.changed_data),
                        'Должны приходить обновленные данные для героя')

    @pytest.mark.parametrize(
        ('invalid_data', 'by_invalid_name'),
        [
            ('', 'с пустым полем "name"'),
            (123, 'со значением не строкового типа int в поле "name"'),
            (True, 'со значением не строкового типа bool в поле "name"'),
            ('PepegaFrog', ', которого нет в базе')
        ]
    )
    @allure.description('Редактирование героя с некорректно заполненным полем "name"')
    def test_edit_character_with_invalid_data(self, reset, auth, invalid_data, by_invalid_name):
        with allure.step('Отправляем запрос на изменение найденного героя с невалидным полем "name"'):
            data = {
                "name": invalid_data,
                "weight": 104,
                "identity": self.changed_data
            }
            response = client.edit_character(json=data, auth=auth)

        with allure.step('Проверяем, что в ответ приходит 400 статус код'):
            assert_that(response.status_code, equal_to(HTTPStatus.BAD_REQUEST))

    @allure.description('Редактирование героя под неавторизованным пользователем')
    def test_edit_character_wo_auth(self, reset, get_exist_hero_name):
        with allure.step('Отправляем запрос на изменение героя, не указывая username и password'):
            data = {
                "name": get_exist_hero_name,
                "weight": 104,
                "identity": self.changed_data
            }
            response = client.edit_character(json=data)

        with allure.step('Проверяем, что в ответ приходит 401 статус код и сообщение об ошибке'):
            assert_that(response.status_code, equal_to(HTTPStatus.UNAUTHORIZED))
            assert_that(response.text, contains_string('You have to login with proper credentials'),
                        'При попытке редактирования данных без авторизации '
                        'должно приходить сообщение о необходимости залогиниться')

    @allure.description('Редактирование данных героя без указания обязательного поля "name"')
    def test_edit_character_wo_required_name(self, reset, auth):
        with allure.step('Отправляем запрос на изменение героя без обязательного поля "name"'):
            data = {
                "weight": 104,
                "identity": self.changed_data
            }
            response = client.edit_character(json=data, auth=auth)

        with allure.step('Проверяем, что в ответ приходит статус код 400 и сообщение об ошибке'):
            assert_that(response.status_code, equal_to(HTTPStatus.BAD_REQUEST))
            assert_that(response.text, contains_string('Missing data for required field'),
                        'Должно приходить сообщение об обязательности заполнения поля')
