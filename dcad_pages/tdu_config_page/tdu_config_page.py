import allure
from selenium.webdriver.chrome.webdriver import WebDriver

from base_page.base_page import BasePage
from dcad_pages.tdu_config_page.tdu_config_filter_component import TduConfigFilterComponent
from elements.button import Button
from elements.input import Input
from elements.text import Text
from tools.routes.dcad_routes import DcadRoutes
from tools.validators import assertions


class TduConfigPage(BasePage):
    """
    Страница Конфигуратор TDU (Config)
    Содержит форму фильтров, дропдаун готовой конфигурации,
    поиск по номеру расчёта и кнопки скачивания (Чертёж, Чертёж в производство, BOM)
    """

    NAME_PAGE = '|Страница конфигуратор ТДУ (config)|'

    def __init__(self, driver: WebDriver, url: str = DcadRoutes.PAGE_CONFIG) -> None:
        super().__init__(driver, url)

        # Components
        self.filter_component = TduConfigFilterComponent(driver)

        # Text
        self._header = Text(
            driver,
            "//strong[text()='Конфигуратор TDU']",
            "Заголовок страницы"
        )

        # Input
        self._input_calculation_number = Input(
            driver,
            "//input[@name='CalculationId']",
            "Номер расчёта"
        )

        # Button
        self._btn_configuration = Button(
            driver,
            "//button[text()='Конфигурация']",
            "Кнопка Конфигурация"
        )
        self._btn_drawing = Button(
            driver,
            "//button[contains(., 'Чертёж') and not(contains(., 'производство'))]",
            "Кнопка Чертёж"
        )
        self._btn_drawing_production = Button(
            driver,
            "//button[contains(., 'Чертёж в производство')]",
            "Кнопка Чертёж в производство"
        )
        self._btn_bom = Button(
            driver,
            "//button[contains(., 'BOM')]",
            "Кнопка BOM"
        )

    def should_header_visible(self) -> None:
        """Проверка отображения заголовка страницы"""
        with allure.step(f'{self.NAME_PAGE} Проверка отображения заголовка "Конфигуратор TDU"'):
            self._header.wait_visible_on_page()

    def get_calculation_number(self) -> str:
        """Получение номера расчёта из input"""
        with allure.step(f'{self.NAME_PAGE} Получение номера расчёта'):
            self._input_calculation_number.wait_visible_on_page(timeout=10.0)
            return self._input_calculation_number.get_value()

    def filling_calculation_number(self, value: str) -> None:
        """
        Ввод номера расчёта в поле поиска
        :param value: Номер расчёта
        """
        with allure.step(f'{self.NAME_PAGE} Ввод номера расчёта: {value}'):
            self._input_calculation_number.clear_input()
            self._input_calculation_number.filling_input(value)
            self._input_calculation_number.should_value_in_input_field(expected_value=value)

    def click_btn_configuration(self) -> None:
        """Клик по кнопке Конфигурация"""
        with allure.step(f'{self.NAME_PAGE} Клик по кнопке Конфигурация'):
            self._btn_configuration.click()

    def should_action_buttons_visible(self) -> None:
        """Проверка отображения кнопок действий после выбора конфигурации"""
        with allure.step(f'{self.NAME_PAGE} Проверка отображения кнопок Чертёж, Чертёж в производство, BOM'):
            self._btn_drawing.wait_visible_on_page()
            self._btn_drawing_production.wait_visible_on_page()
            self._btn_bom.wait_visible_on_page()

    def should_calculation_number_eq(self, expected_value: str) -> None:
        """
        Проверка номера расчёта в поле
        :param expected_value: Ожидаемый номер расчёта
        """
        with allure.step(f'{self.NAME_PAGE} Проверка номера расчёта - {expected_value}'):
            actual = self.get_calculation_number()
            assertions.assert_eq(
                actual_value=actual,
                expected_value=expected_value,
                allure_title='Проверяем номер расчёта в поле',
                error_message=f'Номер расчёта не совпадает. На странице - {actual}; ожидаемое - {expected_value}'
            )