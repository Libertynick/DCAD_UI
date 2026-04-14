import allure
import pytest

from api_testing_project.services.dcad.api.api_tdu_offer import ApiTduOffer


@pytest.mark.stage
@allure.feature('DCAD API')
@allure.story('CAD/TDUOffer')
class TestTduOffer59422:
    """Тесты на DanfossCAD/API/CAD/TDUOffer"""

    PLUGIN_VERSION = '1.0.115.0'
    VALID_CALCULATION_ID = '11649'

    def setup_method(self):
        self.api = ApiTduOffer()

    @allure.title('TDUOffer — успешное получение файла')
    def test_tdu_offer_downloads_file(self):
        """Валидные Auth, CalculationId, PluginVersion → Status=True, Data содержит файл"""
        self.api.get_tdu_offer(calculation_id=self.VALID_CALCULATION_ID, plugin_version=self.PLUGIN_VERSION)
        self.api.check_response_ok()
        self.api.check_file_in_response()

    @allure.title('TDUOffer — неверный Auth токен')
    def test_tdu_offer_invalid_auth(self):
        """Неверный Auth → Status=False, Text='Ваш компьютер не авторизован.'"""
        self.api.get_tdu_offer_raw(
            auth='invalid_token',
            calculation_id=self.VALID_CALCULATION_ID,
            plugin_version=self.PLUGIN_VERSION
        )
        self.api.check_error_response(expected_text='Ваш компьютер не авторизован.')

    @allure.title('TDUOffer — отсутствует заголовок Auth')
    def test_tdu_offer_missing_auth(self):
        """Auth не передан → Status=False, Text='Неправильный запрос.'"""
        self.api.get_tdu_offer_raw(
            auth=None,
            calculation_id=self.VALID_CALCULATION_ID,
            plugin_version=self.PLUGIN_VERSION
        )
        self.api.check_error_response(expected_text='Неправильный запрос.')

    @allure.title('TDUOffer — несуществующий CalculationId')
    def test_tdu_offer_nonexistent_calculation_id(self):
        """CalculationId не существует → Status=False, Text содержит сообщение об ошибке обработки"""
        self.api.get_tdu_offer_raw(calculation_id='999999999', plugin_version=self.PLUGIN_VERSION)
        self.api.check_error_response(
            expected_text='При обработке запроса возникла ошибка. Повторите запрос позднее и, если проблема сохраняется, обратитесь за помощью к представителю Ridan.'
        )

    @allure.title('TDUOffer — пустой CalculationId')
    def test_tdu_offer_empty_calculation_id(self):
        """Пустой CalculationId → Status=False, Text='Запрошенный номер расчета имел некорректный формат.'"""
        self.api.get_tdu_offer_raw(calculation_id='', plugin_version=self.PLUGIN_VERSION)
        self.api.check_error_response(expected_text='Запрошенный номер расчета имел некорректный формат.')

    @allure.title('TDUOffer — отсутствует заголовок PluginVersion')
    def test_tdu_offer_missing_plugin_version(self):
        """PluginVersion не передан → Status=False, Text='Неправильный запрос.'"""
        self.api.get_tdu_offer_raw(calculation_id=self.VALID_CALCULATION_ID, plugin_version=None)
        self.api.check_error_response(expected_text='Неправильный запрос.')