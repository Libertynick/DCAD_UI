import json

import allure
from requests.auth import HTTPBasicAuth
import requests
from config import TestEnvironment

basic_auth = HTTPBasicAuth(TestEnvironment.LOGIN_DAPI, TestEnvironment.PASSWORD_DAPI)


class UnAuthorizedError(Exception):
    """Исключение, возникающее при ошибке 401 Unauthorized"""
    pass


class BadRequest(Exception):
    """Исключение, возникающее при некорректном запросе"""
    pass


class HttpMethods:
    """Стандартные HTTP методы"""

    def __init__(self):
        self.session = requests.Session()

    def get(self, url: str, cookie=None, auth=basic_auth, headers=None):
        with self.session.get(url, cookies=cookie, verify=False, auth=auth, headers=headers) as response:
            with allure.step(f'Запрос get на {url}'):
                try:
                    response.raise_for_status()
                    # response_json = response.json()
                    # status_text_from_response = response_json['status']
                    # status_text_from_response = str(status_text_from_response).lower()
                    # print(status_text_from_response, 'status_text_from_response')
                    # assert status_text_from_response == 'ok', \
                    #     f'Поле status в ответе - ({status_text_from_response}). messages - {response_json["messages"]}\nurl - {url}'
                    return response
                except requests.exceptions.HTTPError as e:
                    if response.status_code == 401:
                        raise UnAuthorizedError(
                            f"Ошибка авторизации: Пользователь не авторизован для доступа к ресурсу {url}.\n {e}")
                    else:
                        raise e

    def post(self, url: str, body: json, headers=None, cookies=None):
        with self.session.post(url, json=body, verify=False, auth=basic_auth, headers=headers,
                               cookies=cookies) as response:
            with allure.step(f'Запрос POST на {url}'):
                allure.attach(json.dumps(body, indent=4, ensure_ascii=False), 'REQUEST', allure.attachment_type.JSON)
                allure.attach(json.dumps(headers, indent=4, ensure_ascii=False), 'HEADERS', allure.attachment_type.JSON)
                try:
                    if response.status_code != 200:
                        print(response.text)
                    response.raise_for_status()
                    return response
                except requests.exceptions.HTTPError as e:
                    if response.status_code == 401:
                        raise UnAuthorizedError(
                            f"Ошибка авторизации: Пользователь не авторизован для доступа к ресурсу {url}.\n {e}")
                    elif response.status_code == 400:
                        raise BadRequest(
                            f'Bad request к url {url}. \n {e}'
                        )
                    else:
                        raise e

    def put(self, url: str, body: json, cookie=''):
        with self.session.put(url, json=body, cookies=cookie) as response:
            with allure.step(f'Запрос PUT на {url}'):
                allure.attach(json.dumps(body, indent=4, ensure_ascii=False), 'REQUEST', allure.attachment_type.JSON)
                try:
                    response.raise_for_status()
                    return response
                except requests.exceptions.HTTPError as e:
                    if response.status_code == 401:
                        raise UnAuthorizedError(
                            f"Ошибка авторизации: Пользователь не авторизован для доступа к ресурсу {url}.\n {e}")
                    else:
                        raise e

    def delete(self, url: str, body: json, cookie=''):
        with self.session.delete(url, json=body, cookies=cookie) as response:
            with allure.step(f'Запрос DELETE на {url}'):
                allure.attach(json.dumps(body, indent=4, ensure_ascii=False), 'REQUEST', allure.attachment_type.JSON)
                try:
                    response.raise_for_status()
                    return response
                except requests.exceptions.HTTPError as e:
                    if response.status_code == 401:
                        raise UnAuthorizedError(
                            f"Ошибка авторизации: Пользователь не авторизован для доступа к ресурсу {url}.\n {e}")
                    else:
                        raise e
