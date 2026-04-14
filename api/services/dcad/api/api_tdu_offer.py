import allure

from api_testing_project.services.base_api import BaseApi


DCAD_CAD_TDU_OFFER_URL = 'http://ruecom-extru-tst.ridancorp.net/DanfossCAD/API/CAD/TDUOffer'
DCAD_CAD_AUTH_TOKEN = 'f747f02181da3099d225d5262e62d9abf0d5960b0ac32752391bdab4963bcbbbe909f047'


class ApiTduOffer(BaseApi):
    """DanfossCAD/API/CAD/TDUOffer"""

    def get_tdu_offer(self, calculation_id: str, plugin_version: str = '1.0.115.0'):
        """
        GET запрос на TDUOffer с валидными данными.
        :return: response объект
        """
        return self.get_tdu_offer_raw(
            calculation_id=calculation_id,
            plugin_version=plugin_version
        )

    def get_tdu_offer_raw(self, calculation_id: str, plugin_version: str = '1.0.115.0', auth: str = DCAD_CAD_AUTH_TOKEN):
        """
        GET запрос на TDUOffer с произвольными заголовками.
        None значения исключаются из заголовков.
        :return: response объект
        """
        headers = {
            'Auth': auth,
            'CalculationId': calculation_id,
            'PluginVersion': plugin_version,
        }
        headers = {k: v for k, v in headers.items() if v is not None}

        with allure.step(f'GET TDUOffer | CalculationId={calculation_id} | PluginVersion={plugin_version}'):
            response = self.http_methods.get(url=DCAD_CAD_TDU_OFFER_URL, auth=None, headers=headers)
            self.response_data = response
            return response

    def check_response_ok(self) -> None:
        """Проверка успешного ответа: статус 200, Status=true, Data не пустой"""
        with allure.step('Проверка успешного ответа TDUOffer'):
            assert self.response_data.status_code == 200, \
                f'Ожидался статус 200, получен {self.response_data.status_code}'
            body = self.response_data.json()
            assert body.get('Status') is not False, \
                f'API вернул ошибку: {body.get("Caption")} — {body.get("Text")}'

    def check_file_in_response(self) -> None:
        """Проверка что поле Data содержит base64 файл"""
        with allure.step('Проверка наличия файла в ответе TDUOffer'):
            body = self.response_data.json()
            data = body.get('Data')
            assert data is not None and len(data) > 0, \
                f'Поле Data пустое или отсутствует. Text: {body.get("Text")}'

    def check_error_response(self, expected_text: str) -> None:
        """
        Проверка негативного ответа: Status=False, Data=None, Text совпадает с ожидаемым.
        :param expected_text: Ожидаемый текст ошибки из поля Text
        """
        with allure.step(f'Проверка ошибки TDUOffer — ожидаем: {expected_text}'):
            assert self.response_data.status_code == 200, \
                f'Ожидался статус 200, получен {self.response_data.status_code}'
            body = self.response_data.json()
            assert body.get('Status') is False, \
                f'Ожидался Status=False, получен {body.get("Status")}'
            assert body.get('Data') is None, \
                f'Ожидался Data=None, получен непустой Data'
            assert body.get('Text') == expected_text, \
                f'Текст ошибки не совпадает.\nОжидалось: {expected_text}\nПолучено: {body.get("Text")}'
