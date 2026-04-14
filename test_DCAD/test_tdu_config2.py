import allure
import pytest

from components.dcad_components.authorization_dcad_page import AuthorizationDcadPage
from dcad_pages.tdu_config_2_page.tdu_config_2_page import ConfiguratorTdu2Page
from dcad_pages.tdu_edit_config_page.tdu_edit_config_page import TduEditConfigPage
from tools.dcad_order_helper import create_offer, should_offer_created


@allure.feature('DCAD')
@allure.story('Тесты на подбор')
@pytest.mark.stage
@pytest.mark.prod
class TestConfig2:
    """Тесты на Конфиг 2"""

    FILTER_PARAMS = {
        "node_type": "TDU.7R",
        "branches": "2",
        "riser": "Слева",
        "inlet_diameter": "20",
        "partner_valve": "Есть",
        "branch_valves": "MVT-R"
    }

    @pytest.fixture(autouse=True)
    def setup(self, browser, dcad_env) -> None:
        self.browser = browser
        self.login = dcad_env['login']
        self.password = dcad_env['password']
        self.auth_dcad = AuthorizationDcadPage(browser, dcad_env['routes'].PAGE_AUTHORIZATION)
        self.config_tdu_2_page = ConfiguratorTdu2Page(browser, dcad_env['routes'].PAGE_CONFIG_2)
        self.tdu_edit_config = TduEditConfigPage(browser)

    def open_and_auth(self, authorization_dcad_fixture) -> None:
        """Открытие страницы авторизации и авторизация"""
        self.auth_dcad.open()
        authorization_dcad_fixture(self.login, self.password)
        self.config_tdu_2_page.open()
        self.config_tdu_2_page.should_header_page_visible()

    def apply_filters(self, page: ConfiguratorTdu2Page):
        """
        Применение фильтров на странице конфигуратора TDU
        :param page: Страница конфигуратора TDU
        """
        page.filter_component.select_node_type(self.FILTER_PARAMS["node_type"])
        page.filter_component.select_branches(self.FILTER_PARAMS["branches"])
        page.filter_component.select_riser(self.FILTER_PARAMS["riser"])
        page.filter_component.select_inlet_diameter(self.FILTER_PARAMS["inlet_diameter"])
        page.filter_component.select_partner_valve(self.FILTER_PARAMS["partner_valve"])
        page.filter_component.select_branch_valves(self.FILTER_PARAMS["branch_valves"])

    @allure.title('Конфигуратор TDU - Список: проверка результатов таблицы после фильтров')
    def test_table_has_results_after_filters_59420(self, authorization_dcad_fixture):
        self.open_and_auth(authorization_dcad_fixture)
        self.apply_filters(self.config_tdu_2_page)
        self.config_tdu_2_page.results_table_component.should_table_title_visible()
        self.config_tdu_2_page.results_table_component.check_all_names_contain(self.FILTER_PARAMS["node_type"])
        self.config_tdu_2_page.results_table_component.check_partner_valve_column(self.FILTER_PARAMS["partner_valve"])
        self.config_tdu_2_page.results_table_component.check_all_articles_not_empty()

        material_code = self.config_tdu_2_page.results_table_component.get_article_by_row(1)
        response = create_offer(material_code=material_code, line_type='TDU')
        should_offer_created(response)

    @allure.title('Конфигуратор TDU - Список: скачивание чертежей всех строк')
    def test_download_drawings_all_rows_58342(self, authorization_dcad_fixture):
        self.open_and_auth(authorization_dcad_fixture)
        self.apply_filters(self.config_tdu_2_page)
        self.config_tdu_2_page.results_table_component.should_table_title_visible()

        rows_count = self.config_tdu_2_page.results_table_component.get_table_rows_count()
        for row_index in range(1, rows_count + 1):
            self.config_tdu_2_page.results_table_component.download_drawing_by_row_index(row_index=row_index)

    @allure.title('Конфигуратор TDU - Список: открытие редактора для всех строк')
    def test_open_editor_all_rows_58342(self, browser, authorization_dcad_fixture):
        self.open_and_auth(authorization_dcad_fixture)
        self.apply_filters(self.config_tdu_2_page)
        self.config_tdu_2_page.results_table_component.should_table_title_visible()

        main_window = browser.current_window_handle
        names = self.config_tdu_2_page.results_table_component.save_list_name()

        with allure.step(f'Проверка кнопки Изменить для каждой конфигурации ТДУ'):
            for row_index, expected_name in enumerate(names, start=1):
                self.config_tdu_2_page.results_table_component.click_modify_by_row_index(row_index=row_index)
                self.tdu_edit_config.should_start_config_by_name_config(expected_start_config=expected_name)

                browser.close()
                browser.switch_to.window(main_window)
