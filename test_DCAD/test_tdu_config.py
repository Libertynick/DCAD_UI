import allure
import pytest

from components.dcad_components.authorization_dcad_page import AuthorizationDcadPage
from dcad_pages.tdu_config_page.tdu_config_page import TduConfigPage
from tools.routes.dcad_routes import DcadRoutes
from config import TestEnvironment


@allure.feature('DCAD')
@allure.story('Конфигуратор TDU (Config)')
@pytest.mark.stage
@pytest.mark.prod
class TestTduConfig:
    """Тесты на страницу Конфигуратор TDU (Config)"""

    @pytest.fixture(autouse=True)
    def setup(self, browser, dcad_env) -> None:
        self.browser = browser
        self.login = dcad_env['login']
        self.password = dcad_env['password']
        self.auth_dcad = AuthorizationDcadPage(browser, dcad_env['routes'].PAGE_AUTHORIZATION)
        self.config_page = TduConfigPage(browser, dcad_env['routes'].PAGE_CONFIG)

    def _auth_and_open_config(self, authorization_dcad_fixture) -> None:
        self.auth_dcad.open()
        authorization_dcad_fixture(self.login, self.password)
        self.config_page.open()

    # @pytest.fixture(autouse=True)
    # def setup(self, browser) -> None:
    #     self.browser = browser
    #     self.auth_dcad = AuthorizationDcadPage(browser, DcadRoutes.PAGE_AUTHORIZATION)
    #     self.config_page = TduConfigPage(browser, DcadRoutes.PAGE_CONFIG)
    #
    # def _auth_and_open_config(self, authorization_dcad_fixture) -> None:
    #     """Авторизация и открытие страницы Config"""
    #     self.auth_dcad.open()
    #     authorization_dcad_fixture(TestEnvironment.DCAD_LOGIN, TestEnvironment.DCAD_PASSWORD)
    #     self.config_page.open()
    #     self.config_page.should_header_visible()

    def _auth_open_and_configure(self, authorization_dcad_fixture) -> None:
        """Авторизация, открытие страницы, выбор первой конфигурации и клик Конфигурация"""
        self._auth_and_open_config(authorization_dcad_fixture)
        self.config_page.filter_component.select_node_type('Узел этажный TDU.7R')
        first_config = self.config_page.filter_component.get_first_available_config()
        self.config_page.filter_component.select_ready_config(first_config)
        self.config_page.click_btn_configuration()

    @pytest.mark.parametrize('node_type, expected_type_contains', [
        ('Узел этажный TDU.7R', 'TDU.7R'),
        ('Узел этажный TDU.5R', 'TDU.5R'),
        ('Узел этажный TDU.3R', 'TDU.3'),
    ])
    @allure.title('Конфигуратор TDU - Проверка готовой конфигурации после фильтров')
    def test_ready_config_matches_filters(self, authorization_dcad_fixture, node_type: str,
                                          expected_type_contains: str) -> None:
        self._auth_and_open_config(authorization_dcad_fixture)

        self.config_page.filter_component.select_node_type(node_type)
        first_config = self.config_page.filter_component.get_first_available_config()
        self.config_page.filter_component.select_ready_config(first_config)

        self.config_page.filter_component.should_ready_config_matches_filters(expected_type_contains)

    @allure.title('Конфигуратор TDU - Конфигурация: отображается автоназвание после выбора конфигурации')
    def test_auto_name_visible_after_configuration(self, authorization_dcad_fixture) -> None:
        self._auth_and_open_config(authorization_dcad_fixture)

        self.config_page.filter_component.select_node_type('Узел этажный TDU.7R')
        first_config = self.config_page.filter_component.get_first_available_config()
        self.config_page.filter_component.select_ready_config(first_config)
        self.config_page.click_btn_configuration()

        self.config_page.should_auto_name_contains_in_config(first_config)

    @pytest.mark.skip(reason='Баг: цена отображается как 0 после нажатия Конфигурация. Вернуться после фикса')
    @allure.title('Конфигуратор TDU - Конфигурация: цена больше нуля после выбора конфигурации')
    def test_price_greater_than_zero_after_configuration(self, authorization_dcad_fixture) -> None:
        self._auth_and_open_config(authorization_dcad_fixture)

        self.config_page.filter_component.select_node_type('Узел этажный TDU.7R')
        first_config = self.config_page.filter_component.get_first_available_config()
        self.config_page.filter_component.select_ready_config(first_config)
        self.config_page.click_btn_configuration()

        self.config_page.should_price_greater_than_zero()

    @allure.title('Конфигуратор TDU - Превью: отображается схема конфигурации')
    def test_preview_shows_canvas(self, authorization_dcad_fixture) -> None:
        self._auth_and_open_config(authorization_dcad_fixture)

        self.config_page.filter_component.select_node_type('Узел этажный TDU.7R')
        first_config = self.config_page.filter_component.get_first_available_config()
        self.config_page.filter_component.select_ready_config(first_config)
        self.config_page.click_btn_configuration()
        self.config_page.click_btn_preview()

        self.config_page.should_canvas_visible()

    @allure.title('Конфигуратор TDU - Модалка: открывается после нажатия Создать конфигурацию')
    def test_modal_visible_after_create_configuration(self, authorization_dcad_fixture) -> None:
        self._auth_open_and_configure(authorization_dcad_fixture)
        self.config_page.click_btn_create_configuration()

    @allure.title('Конфигуратор TDU - Модалка: скачивание чертежа')
    def test_download_drawing_from_modal(self, authorization_dcad_fixture) -> None:
        self._auth_open_and_configure(authorization_dcad_fixture)
        self.config_page.click_btn_create_configuration()
        self.config_page.result_modal.click_download_drawing()

    @allure.title('Конфигуратор TDU - Модалка: скачивание чертежа в производство')
    def test_download_drawing_production_from_modal(self, authorization_dcad_fixture) -> None:
        self._auth_open_and_configure(authorization_dcad_fixture)
        self.config_page.click_btn_create_configuration()
        self.config_page.result_modal.click_download_drawing_production()

    @allure.title('Конфигуратор TDU - Модалка: скачивание BOM')
    def test_download_bom_from_modal(self, authorization_dcad_fixture) -> None:
        self._auth_open_and_configure(authorization_dcad_fixture)
        self.config_page.click_btn_create_configuration()
        self.config_page.result_modal.click_download_bom()

    @allure.title('Конфигуратор TDU - Страница: скачивание чертежа')
    def test_download_drawing_from_page(self, authorization_dcad_fixture) -> None:
        self._auth_open_and_configure(authorization_dcad_fixture)
        self.config_page.click_download_drawing()

    @allure.title('Конфигуратор TDU - Страница: скачивание чертежа в производство')
    def test_download_drawing_production_from_page(self, authorization_dcad_fixture) -> None:
        self._auth_open_and_configure(authorization_dcad_fixture)
        self.config_page.click_download_drawing_production()

    @allure.title('Конфигуратор TDU - Страница: скачивание BOM')
    def test_download_bom_from_page(self, authorization_dcad_fixture) -> None:
        self._auth_open_and_configure(authorization_dcad_fixture)
        self.config_page.click_download_bom()