import uuid
from http import HTTPStatus

import pytest
from hamcrest import assert_that, equal_to, contains_string
from framework.client import HttpClient
import allure

from constants import CHARACTER_PATH


class TestUpdateCharacters:
    changed_data = str(uuid.uuid4())

    @allure.description('Редактирование существующего героя под авторизованным пользователем')
    def test_edit_exist_character(self, reset, get_exist_hero_name, auth):
        allure.step('Достать из базы существующего героя по полю "name"')

        with allure.step('Изменить данные для найденного героя будучи авторизованным'):
            payload = {
                "name": get_exist_hero_name,
                "weight": 104,
                "identity": self.changed_data
            }
            response = HttpClient.edit_character(
                url=CHARACTER_PATH,
                auth=auth,
                json=payload
            )
            assert_that(response.status_code, equal_to(HTTPStatus.OK), 'Должно работать изменение существующего героя')

        with allure.step('Поверить, что герой лежит в базе с обновленным данными'):
            response_after_edit = HttpClient.get_character(url=f'{CHARACTER_PATH}?name={get_exist_hero_name}',
                                                           auth=auth)
            assert_that(response_after_edit.text, contains_string(self.changed_data),
                        'Должны приходить обновленные данные для героя')

    @pytest.mark.parametrize(
        ('invalid_data', 'by_invalid_name'),
        [
            (None, 'cо значением null в поле "name"'),
            ('', 'с незаполненным полем "name"'),
            (123, 'со значением не строкового типа int в поле "name"'),
            (True, 'со значением не строкового типа bool в поле "name"'),
            ('PepegaFrog', ', которого нет в базе')
        ]
    )
    @allure.description('Редактирование героя с некорректно заполненным полем "name"')
    def test_edit_character_with_invalid_data(self, reset, auth, invalid_data, by_invalid_name):
        with allure.step('Изменить данные для найденного героя'):
            payload = {
                "name": invalid_data,
                "weight": 104,
                "identity": self.changed_data
            }
            response = HttpClient.edit_character(
                url=CHARACTER_PATH,
                auth=auth,
                json=payload
            )

        with allure.step('Поверить, что нельзя отредактировать героя'):
            assert_that(response.status_code, equal_to(HTTPStatus.BAD_REQUEST),
                        f'Не должно работать изменение данных героя {by_invalid_name}')

    @allure.description('Редактирование героя под неавторизованным пользователем')
    def test_edit_character_wo_auth(self, reset, get_exist_hero_name):
        with allure.step('Редактировать героя, не указывая username и password'):
            payload = {
                "name": get_exist_hero_name,
                "weight": 104,
                "identity": self.changed_data
            }
            response = HttpClient.edit_character(
                url=CHARACTER_PATH,
                json=payload
            )

        with allure.step('Проверить, что невозможно отредактировать данные героя без авторизации'):
            assert_that(response.status_code, equal_to(HTTPStatus.UNAUTHORIZED),
                        'Не должно работать изменение данных о герое под неавторизованным пользователем')
            assert_that(response.text, contains_string('You have to login with proper credentials'),
                        'При попытке редактирования данных без авторизации '
                        'должно приходить сообщение о необходимости залогиниться')

    @allure.description('Редактирование данных героя без указания обязательного поля "name"')
    def test_edit_character_wo_required_name(self, reset, auth):
        with allure.step('Изменить данные героя без обязательного поля "name"'):
            payload = {
                "weight": 104,
                "identity": self.changed_data
            }
            response = HttpClient.edit_character(
                url=CHARACTER_PATH,
                auth=auth,
                json=payload
            )

        with allure.step('Поверить, что нельзя изменить данные героя'):
            assert_that(response.status_code, equal_to(HTTPStatus.BAD_REQUEST),
                        'Не должно работать изменение данных героя без указания обязательного поля "name"')
            assert_that(response.text, contains_string('Missing data for required field'),
                        'Должно приходить сообщение об обязательности заполнения поля')
