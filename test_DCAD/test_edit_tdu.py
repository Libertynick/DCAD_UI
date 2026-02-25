import allure
import pytest

from base_page.base_page import BasePage
from components.dcad_components.authorization_dcad_page import AuthorizationDcadPage
from dcad_pages.tdu_config_2_page.tdu_config_2_page import ConfiguratorTdu2Page
from dcad_pages.tdu_edit_config_page.tdu_edit_config_page import TduEditConfigPage
from tools.routes.dcad_routes import DcadRoutes
from config import TestEnvironment


@allure.feature('DCAD')
@allure.story('Редактор конфигурации TDU')
@pytest.mark.stage
class TestTduEditConfig:
    """Тесты на Редактор конфигурации TDU"""

    @pytest.fixture(autouse=True)
    def setup(self, browser):
        self.browser = browser
        self.page_base = BasePage(browser)
        self.auth_dcad = AuthorizationDcadPage(browser, DcadRoutes.PAGE_AUTHORIZATION)
        self.config_tdu_2_page = ConfiguratorTdu2Page(browser, DcadRoutes.PAGE_CONFIG_2)
        self.edit_page = TduEditConfigPage(browser)

    def _open_editor_for_row(self, authorization_dcad_fixture, row_index: int) -> tuple[str, float]:
        """
        Авторизация, открытие Config2 и редактора для указанной строки
        :param authorization_dcad_fixture: Фикстура авторизации
        :param row_index: Номер строки в таблице (начиная с 1)
        :return: (название конфигурации, цена) из таблицы Config2
        """
        self.auth_dcad.open()
        authorization_dcad_fixture(TestEnvironment.DCAD_LOGIN, TestEnvironment.DCAD_PASSWORD)
        self.config_tdu_2_page.open()
        self.config_tdu_2_page.should_header_page_visible()
        self.config_tdu_2_page.results_table_component.should_table_title_visible()

        expected_name = self.config_tdu_2_page.results_table_component.get_name_by_row(row_index)
        expected_price = self.config_tdu_2_page.results_table_component.get_price_by_row(row_index)

        self.config_tdu_2_page.results_table_component.click_modify_by_row_index(row_index=row_index)

        # Разбить метод на несколько по логическому действию
        return expected_name, expected_price

    @allure.title('Редактор TDU: кнопка Цена показывает корректное название и цену')
    def test_price_button_shows_correct_name_and_price(self, authorization_dcad_fixture) -> None:
        expected_name, expected_price = self._open_editor_for_row(authorization_dcad_fixture, row_index=1)

        self.edit_page.click_price_button()
        self.edit_page.should_result_name_eq(expected_name)
        self.edit_page.should_result_price_within_tolerance(expected_price)

    @allure.title('Редактор TDU: кнопка Цена показывает схему конфигурации')
    def test_price_button_shows_canvas(self, authorization_dcad_fixture) -> None:
        self._open_editor_for_row(authorization_dcad_fixture, row_index=1)

        self.edit_page.click_price_button()
        self.edit_page.should_canvas_visible()

    @allure.title('Редактор TDU: создать расчёт открывает модалку и скачивает чертёж')
    def test_create_calculation_and_download_drawing(self, authorization_dcad_fixture) -> None:
        self._open_editor_for_row(authorization_dcad_fixture, row_index=1)

        self.edit_page.click_create_calculation()
        self.edit_page.result_modal.click_download_drawing()

    @allure.title('Редактор TDU: изменение диаметра вводной группы меняет название конфигурации')
    def test_change_inlet_diameter_changes_name(self, authorization_dcad_fixture) -> None:
        self._open_editor_for_row(authorization_dcad_fixture, row_index=1)
        # Значения вынести в отдельные переменные
        self.edit_page.select_inlet_diameter('20')
        self.edit_page.click_price_button()
        self.edit_page.should_result_name_contains('20')

    @allure.title('Редактор TDU: изменение клапана-партнёра меняет цену')
    def test_change_partner_valve_changes_price(self, authorization_dcad_fixture) -> None:
        self._open_editor_for_row(authorization_dcad_fixture, row_index=1)

        self.edit_page.click_price_button()
        price_before = self.edit_page.get_result_price()

        self.edit_page.select_partner_valve('MVT-R 20')
        self.edit_page.click_price_button()
        self.edit_page.should_result_price_changed(price_before)

    @allure.title('Редактор TDU: снятие чекбокса Кронштейны меняет цену')
    def test_uncheck_brackets_changes_price(self, authorization_dcad_fixture) -> None:
        self._open_editor_for_row(authorization_dcad_fixture, row_index=1)

        self.edit_page.click_price_button()
        price_before = self.edit_page.get_result_price()

        self.edit_page.click_checkbox_brackets()
        self.edit_page.click_price_button()
        self.edit_page.should_result_price_changed(price_before)
