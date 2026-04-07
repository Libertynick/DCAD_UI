import allure
import pytest

from components.dcad_components.authorization_dcad_page import AuthorizationDcadPage
from dcad_pages.wdu_config_page.wdu_config_page import WduConfigPage


@allure.feature('DCAD')
@allure.story('Конфигуратор ВДУ')
@pytest.mark.stage
@pytest.mark.prod
class TestWduConfig:
    """Тесты на страницу Конфигуратор ВДУ"""

    PARAMS = {
        'node_type': 'Узел этажный с редуктором на вводе/на отводах/без [подходит для ХВС, ГВС (T3)]',
        'branches': '3',
        'connection': 'Левое',
        'collector': 'Квадратное сечение Ду40',
        'reducer': 'Нет',
        'branch_dn': '15',
        'inlet_dn': '15',
        'air_vent': 'Нет',
        'drainage': 'Нет',
        'accounting': 'Проставки на каждый отвод DN15',
        'kip': 'Без КИП',
        'filter_inlet': True,
        'outlets_up': True,
        'return_valve': True,
        'extra_filter': False,
        'extra_valve': False,
    }

    @pytest.fixture(autouse=True)
    def setup(self, browser, dcad_env) -> None:
        self.browser = browser
        self.login = dcad_env['login']
        self.password = dcad_env['password']
        self.auth_dcad = AuthorizationDcadPage(browser, dcad_env['routes'].PAGE_AUTHORIZATION)
        self.wdu_page = WduConfigPage(browser, dcad_env['routes'].PAGE_WDU)

    def _auth_and_open(self, authorization_dcad_fixture) -> None:
        """Авторизация и открытие страницы ВДУ"""
        self.auth_dcad.open()
        authorization_dcad_fixture(self.login, self.password)
        self.wdu_page.open()
        self.wdu_page.should_header_visible()

    def _auth_open_and_save(self, authorization_dcad_fixture) -> None:
        """Авторизация, открытие, выбор параметров и сохранение расчёта"""
        self._auth_and_open(authorization_dcad_fixture)
        self.wdu_page.params_component.select_node_type(self.PARAMS['node_type'])
        self.wdu_page.params_component.select_branches(self.PARAMS['branches'])
        self.wdu_page.params_component.select_connection(self.PARAMS['connection'])
        self.wdu_page.params_component.select_collector(self.PARAMS['collector'])
        self.wdu_page.params_component.select_reducer(self.PARAMS['reducer'])
        self.wdu_page.params_component.select_branch_dn(self.PARAMS['branch_dn'])
        self.wdu_page.params_component.select_inlet_dn(self.PARAMS['inlet_dn'])
        self.wdu_page.click_save_calculation()
        self.wdu_page.should_calculation_number_filled()
        self.wdu_page.additional_options_component.select_air_vent(self.PARAMS['air_vent'])
        self.wdu_page.additional_options_component.select_drainage(self.PARAMS['drainage'])
        self.wdu_page.additional_options_component.select_accounting(self.PARAMS['accounting'])
        self.wdu_page.additional_options_component.select_kip(self.PARAMS['kip'])

    @allure.title('Конфигуратор ВДУ - Сохранение расчёта и появление номера WDU')
    def test_save_calculation_number_appears(self, authorization_dcad_fixture) -> None:
        self._auth_open_and_save(authorization_dcad_fixture)

    @allure.title('Конфигуратор ВДУ - Скачивание чертежа')
    def test_download_drawing(self, authorization_dcad_fixture) -> None:
        self._auth_open_and_save(authorization_dcad_fixture)
        self.wdu_page.click_download_drawing()

    @allure.title('Конфигуратор ВДУ - Скачивание чертежа в производство')
    def test_download_drawing_production(self, authorization_dcad_fixture) -> None:
        self._auth_open_and_save(authorization_dcad_fixture)
        self.wdu_page.click_download_drawing_production()

    @allure.title('Конфигуратор ВДУ - Скачивание BOM')
    def test_download_bom(self, authorization_dcad_fixture) -> None:
        self._auth_open_and_save(authorization_dcad_fixture)
        self.wdu_page.click_download_bom()

    @allure.title('Конфигуратор ВДУ - Кнопки скачивания скрыты до сохранения')
    def test_download_buttons_hidden_before_save(self, authorization_dcad_fixture) -> None:
        self._auth_and_open(authorization_dcad_fixture)
        self.wdu_page.should_download_buttons_not_visible()

    @allure.title('Конфигуратор ВДУ - Поиск по номеру расчёта')
    def test_search_by_calculation_number(self, authorization_dcad_fixture) -> None:
        self._auth_open_and_save(authorization_dcad_fixture)
        calc_number = self.wdu_page.get_calculation_number()
        self.wdu_page.fill_calculation_number(calc_number)
        self.wdu_page.click_search()
        self.wdu_page.should_calculation_number_filled()

    @allure.title('Конфигуратор ВДУ - Параметры сохраняются и загружаются корректно')
    def test_params_saved_and_loaded_after_search(self, authorization_dcad_fixture) -> None:
        self._auth_open_and_save(authorization_dcad_fixture)
        calc_number = self.wdu_page.get_calculation_number()
        self.wdu_page.fill_calculation_number(calc_number)
        self.wdu_page.click_search()
        self.wdu_page.should_calculation_number_filled()
        self.wdu_page.params_component.should_params_match(self.PARAMS)
        self.wdu_page.additional_options_component.should_additional_params_match(self.PARAMS)