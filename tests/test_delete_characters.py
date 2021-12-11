import urllib.parse

import pytest
from hamcrest import assert_that, equal_to, contains_string
from framework.client import HttpClient
import allure


class TestDeleteCharacters:

    @allure.description('Удаление существующего героя под авторизованным пользователем')
    def test_delete_exist_character(self, reset, get_exist_hero_name, auth):
        allure.step('Достать из базы существующего героя по полю "name"')

        with allure.step('Удалить найденного героя будучи авторизованным'):
            response = HttpClient.delete_character(
                url=f'/character?name={urllib.parse.quote_plus(get_exist_hero_name)}',
                auth=auth
            )
            assert_that(response.status_code, equal_to(200), 'Должно работать удаление существующего героя')

        with allure.step('Поверить, что удаленного героя больше нет в базе'):
            response_after_delete = HttpClient.get_character(url=f'/character?name={get_exist_hero_name}',
                                                             auth=auth)
            assert_that(response_after_delete.status_code, equal_to(400), 'Удаленного героя не должно быть в базе')

    @allure.description('Удаление героя под неавторизованным пользователем')
    def test_delete_character_wo_auth(self, reset, get_exist_hero_name):
        with allure.step('Удалить героя, не указывая username и password'):
            response = HttpClient.delete_character(
                url=f'/character?name={urllib.parse.quote_plus(get_exist_hero_name)}',
            )

        with allure.step('Поверить, что нельзя удалить героя'):
            assert_that(response.status_code, equal_to(401),
                        'Нельзя удалить героя под неавторизованным пользователем')
            assert_that(response.text, contains_string('You have to login with proper credentials'),
                        'При попытке удалить героя без авторизации '
                        'должно приходить сообщение о необходимости залогиниться')

    @pytest.mark.parametrize(
        ('invalid_data', 'by_invalid_name'),
        [
            (None, 'cо значением null в поле "name"'),
            ('', 'с незаполненным полем "name"'),
            (123, 'со значением не строкового типа int в поле "name"'),
            (True, 'со значением не строкового типа bool в поле "name"'),
            ('Pepega', ', которого нет в базе')
        ]
    )
    @allure.description('Удаление героя c некорректно заполненным полем "name"')
    def test_delete_character_with_invalid_name(self, reset, auth, invalid_data, by_invalid_name):
        with allure.step(f'Удалить героя {by_invalid_name}'):
            response = HttpClient.delete_character(
                url=f'/character?name={invalid_data}',
                auth=auth
            )

        with allure.step('Поверить, что нельзя удалить героя'):
            assert_that(response.status_code, equal_to(400),
                        f'Нельзя удалить героя {by_invalid_name}')

    @allure.description('Удаление героя без обязательного поля "name"')
    def test_delete_character_wo_required_name(self, reset, auth):
        with allure.step('Удалить героя без обязательного поля "name"'):

            response = HttpClient.delete_character(
                url='/character',
                auth=auth,
            )

        with allure.step('Поверить, что нельзя удалить героя'):
            assert_that(response.status_code, equal_to(400),
                        f'Нельзя удалить героя без обязательного поля "name"')
            assert_that(response.text, contains_string('name parameter is required'),
                        f'Должно приходить сообщение об обязательности заполнения поля')
