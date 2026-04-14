import allure
import pytest

from base_page.base_page import BasePage
from components.dcad_components.authorization_dcad_page import AuthorizationDcadPage
from dcad_pages.tdu_config_2_page.tdu_config_2_page import ConfiguratorTdu2Page
from dcad_pages.tdu_edit_config_page.tdu_edit_config_page import TduEditConfigPage

@allure.feature('DCAD')
@allure.story('Редактор конфигурации TDU')
@pytest.mark.stage
@pytest.mark.prod
class TestTduEditConfig:
    """Тесты на Редактор конфигурации TDU"""

    @pytest.fixture(autouse=True)
    def setup(self, browser, dcad_env) -> None:
        self.browser = browser
        self.login = dcad_env['login']
        self.password = dcad_env['password']
        self.page_base = BasePage(browser)
        self.auth_dcad = AuthorizationDcadPage(browser, dcad_env['routes'].PAGE_AUTHORIZATION)
        self.config_tdu_2_page = ConfiguratorTdu2Page(browser, dcad_env['routes'].PAGE_CONFIG_2)
        self.edit_page = TduEditConfigPage(browser)

    def _auth_and_open_config2(self, authorization_dcad_fixture) -> None:
        """Авторизация и открытие страницы Config2"""
        self.auth_dcad.open()
        authorization_dcad_fixture(self.login, self.password)
        self.config_tdu_2_page.open()
        self.config_tdu_2_page.should_header_page_visible()
        self.config_tdu_2_page.results_table_component.should_table_title_visible()

    def _get_row_data(self, row_index: int) -> tuple[str, float]:
        """
        Получение данных строки из таблицы Config2
        :param row_index: Номер строки (начиная с 1)
        :return: (название конфигурации, цена)
        """
        expected_name = self.config_tdu_2_page.results_table_component.get_name_by_row(row_index)
        expected_price = self.config_tdu_2_page.results_table_component.get_price_by_row(row_index)
        return expected_name, expected_price

    @allure.title('Редактор TDU: кнопка Цена показывает корректное название и цену')
    def test_price_button_shows_correct_name_and_price_58342(self, authorization_dcad_fixture) -> None:
        self._auth_and_open_config2(authorization_dcad_fixture)
        expected_name, expected_price = self._get_row_data(row_index=1)
        self.config_tdu_2_page.results_table_component.click_modify_by_row_index(row_index=1)

        self.edit_page.click_price_button()
        self.edit_page.should_result_name_eq(expected_name)
        self.edit_page.should_result_price_within_tolerance(expected_price)

    @allure.title('Редактор TDU: кнопка Цена показывает схему конфигурации')
    def test_price_button_shows_canvas_58342(self, authorization_dcad_fixture) -> None:
        self._auth_and_open_config2(authorization_dcad_fixture)
        self._get_row_data(row_index=1)
        self.config_tdu_2_page.results_table_component.click_modify_by_row_index(row_index=1)

        self.edit_page.click_price_button()
        self.edit_page.should_canvas_visible()

    @allure.title('Редактор TDU: создать расчёт открывает модалку и скачивает чертёж')
    def test_create_calculation_and_download_drawing_58342(self, authorization_dcad_fixture) -> None:
        self._auth_and_open_config2(authorization_dcad_fixture)
        self._get_row_data(row_index=1)
        self.config_tdu_2_page.results_table_component.click_modify_by_row_index(row_index=1)

        self.edit_page.click_create_calculation()
        self.edit_page.result_modal.click_download_drawing()

    @allure.title('Редактор TDU: изменение диаметра вводной группы меняет название конфигурации')
    def test_change_inlet_diameter_changes_name_58342(self, authorization_dcad_fixture) -> None:
        inlet_diameter = '20'

        self._auth_and_open_config2(authorization_dcad_fixture)
        self._get_row_data(row_index=1)
        self.config_tdu_2_page.results_table_component.click_modify_by_row_index(row_index=1)

        self.edit_page.select_inlet_diameter(inlet_diameter)
        self.edit_page.click_price_button()
        self.edit_page.should_result_name_contains(inlet_diameter)

    @allure.title('Редактор TDU: изменение клапана-партнёра меняет цену')
    def test_change_partner_valve_changes_price_58342(self, authorization_dcad_fixture) -> None:
        partner_value = 'MVT-R 20'

        self._auth_and_open_config2(authorization_dcad_fixture)
        self._get_row_data(row_index=1)
        self.config_tdu_2_page.results_table_component.click_modify_by_row_index(row_index=1)

        self.edit_page.click_price_button()
        price_before = self.edit_page.get_result_price()

        self.edit_page.select_partner_valve(partner_value)
        self.edit_page.click_price_button()
        self.edit_page.should_result_price_changed(price_before)

    @allure.title('Редактор TDU: снятие чекбокса Кронштейны меняет цену')
    def test_uncheck_brackets_changes_price_58342(self, authorization_dcad_fixture) -> None:
        self._auth_and_open_config2(authorization_dcad_fixture)
        self._get_row_data(row_index=1)
        self.config_tdu_2_page.results_table_component.click_modify_by_row_index(row_index=1)

        self.edit_page.click_price_button()
        price_before = self.edit_page.get_result_price()

        self.edit_page.uncheck_brackets()
        self.edit_page.click_price_button()
        self.edit_page.should_result_price_changed(price_before)