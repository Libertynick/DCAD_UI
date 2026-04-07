import allure
from selenium.webdriver.chrome.webdriver import WebDriver

from base_page.base_page import BasePage
from dcad_pages.wdu_config_page.wdu_params_component import WduParamsComponent
from dcad_pages.wdu_config_page.wdu_additional_options_component import WduAdditionalOptionsComponent
from elements.button import Button
from elements.input import Input
from elements.text import Text
from tools.validators import assertions


class WduConfigPage(BasePage):
    """
    Страница Конфигуратор ВДУ
    Содержит компонент основных параметров и кнопки:
    Найти, Сохранить расчет, Чертёж, Чертёж в производство, BOM
    """

    NAME_PAGE = '|Страница конфигуратор ВДУ|'

    def __init__(self, driver: WebDriver, url: str = None) -> None:
        super().__init__(driver, url)

        # Component
        self.params_component = WduParamsComponent(driver)
        self.additional_options_component = WduAdditionalOptionsComponent(driver)

        # Text
        self._header = Text(
            driver,
            "//p[@class='lead']//strong[contains(text(), 'Конфигуратор ВДУ')]",
            "Заголовок страницы"
        )

        # Input
        self._input_calc_id = Input(
            driver,
            "//input[@id='calcId']",
            "Поле номера расчёта"
        )

        # Button
        self._btn_search = Button(
            driver,
            "//button[@id='searchCalc']",
            "Кнопка Найти"
        )
        self._btn_save = Button(
            driver,
            "//button[@id='saveCalc']",
            "Кнопка Сохранить расчет"
        )
        self._btn_drawing = Button(
            driver,
            "//a[@id='GenerateDraw']",
            "Кнопка Чертёж"
        )
        self._btn_drawing_production = Button(
            driver,
            "//a[@id='GenerateDrawFactory']",
            "Кнопка Чертёж в производство"
        )
        self._btn_bom = Button(
            driver,
            "//a[@id='GenerateBOM']",
            "Кнопка BOM"
        )

    def should_header_visible(self) -> None:
        """Проверка отображения заголовка страницы"""
        with allure.step(f'{self.NAME_PAGE} Проверка отображения заголовка страницы'):
            self._header.wait_visible_on_page()

    def get_calculation_number(self) -> str:
        """
        Получение номера расчёта из поля ввода
        :return: Номер расчёта (например WDU1011984)
        """
        with allure.step(f'{self.NAME_PAGE} Получение номера расчёта'):
            self._input_calc_id.wait_visible_on_page()
            return self._input_calc_id.get_value()

    def click_save_calculation(self) -> None:
        """Клик по кнопке Сохранить расчет"""
        with allure.step(f'{self.NAME_PAGE} Клик по кнопке Сохранить расчет'):
            self._btn_save.scroll_to_elem_js()
            self._btn_save.click()

    def should_calculation_number_filled(self) -> None:
        """Проверка что номер расчёта появился в поле после сохранения"""
        with allure.step(f'{self.NAME_PAGE} Проверка что номер расчёта заполнен'):
            self._btn_drawing.wait_visible_on_page(timeout=15.0)
            calc_number = self.get_calculation_number()
            assertions.assert_contains(
                actual_value=calc_number,
                expected_contains='WDU',
                allure_title='Проверяем что номер расчёта содержит WDU',
                error_message=f'Номер расчёта не содержит WDU, получили: {calc_number}'
            )

    def click_download_drawing(self) -> None:
        """Клик по кнопке Чертёж и проверка скачивания zip файла"""
        with allure.step(f'{self.NAME_PAGE} Скачивание чертежа'):
            number = self.get_calculation_number().replace('WDU', '')
            self._btn_drawing.scroll_to_elem_js()
            self._btn_drawing.click(timeout=10.0)
            self.find_file_by_substrings_in_download_folder(['WDU', f'исп.{number}', '.zip'])

    def click_download_drawing_production(self) -> None:
        """Клик по кнопке Чертёж в производство и проверка скачивания zip файла"""
        with allure.step(f'{self.NAME_PAGE} Скачивание чертежа в производство'):
            number = self.get_calculation_number().replace('WDU', '')
            self._btn_drawing_production.scroll_to_elem_js()
            self._btn_drawing_production.click(timeout=10.0)
            self.find_file_by_substrings_in_download_folder(['WDU', f'исп.{number}', '.zip'])

    def click_download_bom(self) -> None:
        """Клик по кнопке BOM и проверка скачивания xlsx файла"""
        with allure.step(f'{self.NAME_PAGE} Скачивание BOM'):
            calc_number = self.get_calculation_number()
            expected_file_name = f'BOM_{calc_number}.xlsx'
            self.delete_file_by_name_in_download_folder(expected_file_name)
            self._btn_bom.scroll_to_elem_js()
            self._btn_bom.click(timeout=10.0)
            self.checking_the_download_document_in_the_download_folder(expected_file_name)
            self.delete_file_by_name_in_download_folder(expected_file_name)

    def fill_calculation_number(self, calc_number: str) -> None:
        """
        Ввод номера расчёта в поле поиска
        :param calc_number: Номер расчёта
        """
        with allure.step(f'{self.NAME_PAGE} Ввод номера расчёта: {calc_number}'):
            self._input_calc_id.clear_input()
            self._input_calc_id.filling_input(calc_number)

    def click_search(self) -> None:
        """Клик по кнопке Найти и ожидание загрузки результата"""
        with allure.step(f'{self.NAME_PAGE} Клик по кнопке Найти'):
            self._btn_search.click()
            self._btn_drawing.wait_visible_on_page(timeout=15.0)

    def should_download_buttons_not_visible(self) -> None:
        """Проверка что кнопки скачивания скрыты до сохранения расчёта"""
        with allure.step(f'{self.NAME_PAGE} Проверка что кнопки Чертёж/BOM не видны'):
            self._btn_drawing.wait_no_visible_on_page(timeout=3.0)
            self._btn_drawing_production.wait_no_visible_on_page(timeout=3.0)
            self._btn_bom.wait_no_visible_on_page(timeout=3.0)