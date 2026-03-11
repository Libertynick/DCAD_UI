import allure
import pytest

from components.dcad_components.authorization_dcad_page import AuthorizationDcadPage
from dcad_pages.tdu_config_page.tdu_config_page import TduConfigPage
from tools.routes.dcad_routes import DcadRoutes
from config import TestEnvironment


@allure.feature('DCAD')
@allure.story('Конфигуратор TDU (Config)')
@pytest.mark.stage
class TestTduConfig:
    """Тесты на страницу Конфигуратор TDU (Config)"""

    @pytest.fixture(autouse=True)
    def setup(self, browser) -> None:
        self.browser = browser
        self.auth_dcad = AuthorizationDcadPage(browser, DcadRoutes.PAGE_AUTHORIZATION)
        self.config_page = TduConfigPage(browser, DcadRoutes.PAGE_CONFIG)

    def _auth_and_open_config(self, authorization_dcad_fixture) -> None:
        """Авторизация и открытие страницы Config"""
        self.auth_dcad.open()
        authorization_dcad_fixture(TestEnvironment.DCAD_LOGIN, TestEnvironment.DCAD_PASSWORD)
        self.config_page.open()
        self.config_page.should_header_visible()

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