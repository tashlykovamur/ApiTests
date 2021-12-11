import pytest
from hamcrest import assert_that, equal_to, contains_string
from framework.client import HttpClient
import allure
import urllib.parse


class TestGetCharacters:

    @allure.description('Получение всех существующих героев из базы под авторизованным пользователем')
    def test_get_all_characters(self, reset, get_exist_hero_name, auth):
        with allure.step('Достать из базы информацию обо всех героях'):
            response = HttpClient.get_characters(
                url=f'/characters',
                auth=auth
            )

        with allure.step('Проверить, что работает получение данных о героях'):
            assert_that(response.status_code, equal_to(200), 'Должно работать получение информации обо всех героях')

    @allure.description('Получение существующего героя под авторизованным пользователем')
    def test_get_exist_character(self, reset, get_exist_hero_name, auth):
        allure.step('Достать из базы существующего героя по полю "name"')

        with allure.step('Запросить информацию о найденном герое'):
            response = HttpClient.get_character(
                url=f'/character?name={urllib.parse.quote_plus(get_exist_hero_name)}',
                auth=auth
            )

        with allure.step('Проверить, что работает получение данных героя'):
            assert_that(response.status_code, equal_to(200), 'Должно работать получение данных существующего героя')

    @allure.description('Получение данных о героях под неавторизованным пользователем')
    def test_get_characters_wo_auth(self, reset):
        with allure.step('Запросить данные о героях без ввода username и password'):
            response = HttpClient.get_characters(
                url=f'/characters',
            )

        with allure.step('Проверить, что невозможно получить данные о героях'):
            assert_that(response.status_code, equal_to(401),
                        'Нельзя получить данные о героях под неавторизованным пользователем')
            assert_that(response.text, contains_string('You have to login with proper credentials'),
                        'При попытке получить данные без авторизации '
                        'должно приходить сообщение о необходимости залогиниться')

    @allure.description('Получение данные о герое под неавторизованным пользователем')
    def test_get_all_characters_wo_auth(self, reset, get_exist_hero_name):
        with allure.step('Получить данные о герое, не указывая username и password'):
            response = HttpClient.get_character(
                url=f'/character?name={urllib.parse.quote_plus(get_exist_hero_name)}',
            )

        with allure.step('Проверить, что нельзя получить данные о герое'):
            assert_that(response.status_code, equal_to(401),
                        'Нельзя получить данные о герое под неавторизованным пользователем')
            assert_that(response.text, contains_string('You have to login with proper credentials'),
                        'При попытке получить данные о герое без авторизации '
                        'должно приходить сообщение о необходимости залогиниться')

    @allure.description('Получение данные о герое без указания обязательного поля "name"')
    def test_get_character_wo_required_name(self, reset, auth):
        with allure.step('Получить данные о герое без указания обязательного поля "name"'):
            response = HttpClient.get_character(
                url='/character',
                auth=auth,
            )

        with allure.step('Проверить, что нельзя получение данные о героях'):
            assert_that(response.status_code, equal_to(400),
                        f'Нельзя получить данные о герое без указания обязательного поля "name"')
            assert_that(response.text, contains_string('name parameter is required'),
                        f'Должно приходить сообщение об обязательности заполнения поля')

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
    @allure.description('Получение данных о герое c некорректно заполненным полем "name"')
    def test_get_character_with_invalid_name(self, reset, auth, invalid_data, by_invalid_name):
        with allure.step(f'Запросить информацию о герое {by_invalid_name}'):
            response = HttpClient.get_character(
                url=f'/character?name={invalid_data}',
                auth=auth
            )

        with allure.step('Проверить, что работает получение данных о герое'):
            assert_that(response.status_code, equal_to(400),
                        f'Нельзя получить информацию о герое {by_invalid_name}')
