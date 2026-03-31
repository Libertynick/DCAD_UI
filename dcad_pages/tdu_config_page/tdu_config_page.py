import allure
from selenium.webdriver.chrome.webdriver import WebDriver

from base_page.base_page import BasePage
from dcad_pages.tdu_config_page.tdu_config_filter_component import TduConfigFilterComponent
from elements.button import Button
from elements.input import Input
from elements.text import Text
from tools.routes.dcad_routes import DcadRoutes
from tools.validators import assertions
from dcad_pages.tdu_config_page.tdu_config_modal_component import TduConfigModalComponent


class TduConfigPage(BasePage):
    """
    Страница Конфигуратор TDU (Config)
    Содержит форму фильтров, дропдаун готовой конфигурации,
    поиск по номеру расчёта и кнопки скачивания (Чертёж, Чертёж в производство, BOM)
    """

    NAME_PAGE = '|Страница конфигуратор ТДУ (config)|'

    #def __init__(self, driver: WebDriver, url: str = DcadRoutes.PAGE_CONFIG) -> None:
    def __init__(self, driver: WebDriver, url: str = None) -> None:
        super().__init__(driver, url)

        # Components
        self.filter_component = TduConfigFilterComponent(driver)
        self.result_modal = TduConfigModalComponent(driver)

        # Text
        self._header = Text(
            driver,
            "//strong[text()='Конфигуратор TDU']",
            "Заголовок страницы"
        )
        self._canvas_draw = Text(
            driver,
            "//canvas[@id='draw']",
            "Схема конфигурации"
        )

        # Input
        self._input_calculation_number = Input(
            driver,
            "//input[@name='CalculationId']",
            "Номер расчёта"
        )
        self._auto_name = Input(
            driver,
            "//input[@id='autoName']",
            "Автоназвание"
        )
        self._price = Input(
            driver,
            "//input[@id='pricePreview']",
            "Цена, у.е. с НДС"
        )

        # Button
        self._btn_configuration = Button(
            driver,
            "//button[@data-bind='click: LoadTDUConfigByCalculationId']",
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
            "//a[@class='btn btn-secondary']",
            "Кнопка BOM"
        )

        self._btn_preview = Button(
            driver,
            "//button[@data-bind='click: CalculationPreview']",
            "Кнопка Превью"
        )

        self._btn_create_configuration = Button(
            driver,
            "//button[@data-bind='click: CreateCalculation']",
            "Кнопка Создать конфигурацию"
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

    def get_auto_name(self) -> str:
        """Получение автоназвания конфигурации"""
        with allure.step(f'{self.NAME_PAGE} Получение автоназвания'):
            self._auto_name.wait_visible_on_page(timeout=10.0)
            self._auto_name.scroll_to_elem_js()
            return self._auto_name.get_value()

    def should_auto_name_contains_in_config(self, selected_config: str) -> None:
        """
        Проверка, что автоназвание входит в название выбранной конфигурации
        :param selected_config: Название выбранной конфигурации из дропдауна
        """
        with allure.step(f'{self.NAME_PAGE} Проверка, что автоназвание входит в выбранную конфигурацию'):
            actual = self.get_auto_name()
            assertions.assert_contains(
                actual_value=selected_config,
                expected_contains=actual,
                allure_title='Проверяем что автоназвание входит в название конфигурации',
                error_message=f'Автоназвание - {actual} не входит в конфигурацию - {selected_config}'
            )

    def get_price(self) -> float:
        """Получение цены конфигурации"""
        with allure.step(f'{self.NAME_PAGE} Получение цены конфигурации'):
            self._price.wait_visible_on_page(timeout=10.0)
            self._price.scroll_to_elem_js()
            return self._price.get_float_value_from_line()

    def should_price_greater_than_zero(self) -> None:
        """Проверка цены после нажатия кнопки конфигурации"""
        with allure.step(f'{self.NAME_PAGE} Проверка, что цена больше нуля'):
            self._price.wait_visible_on_page(timeout=10.0)
            self._price.scroll_to_elem_js()
            price = self._price.get_float_value_from_input()
            assertions.assert_greater_than(
                greater_value=price,
                less_value=0,
                allure_title='Проверяем что цена больше нуля',
                error_message=f'Цена равна нулю или отрицательная - {price}'
            )

    def click_btn_preview(self) -> None:
        """Клик по кнопке Превью"""
        with allure.step(f'{self.NAME_PAGE} Клик по кнопке Превью'):
            self._btn_preview.scroll_to_elem_js()
            self._btn_preview.click(timeout=10.0)

    def should_canvas_visible(self) -> None:
        """Проверка отображения схемы конфигурации"""
        with allure.step(f'{self.NAME_PAGE} Проверка отображения схемы конфигурации'):
            self._canvas_draw.scroll_to_elem_js()
            self._canvas_draw.wait_visible_on_page(timeout=15.0)

    def click_btn_create_configuration(self) -> None:
        """Клик по кнопке Создать конфигурацию и ожидание модального окна"""
        with allure.step(f'{self.NAME_PAGE} Клик по кнопке Создать конфигурацию'):
            self._btn_create_configuration.scroll_to_elem_js()
            self._btn_create_configuration.click(timeout=10.0)
            self.result_modal.should_modal_visible()

    def click_download_drawing(self) -> None:
        """Клик по кнопке Чертёж и проверка скачивания zip файла"""
        with allure.step(f'{self.NAME_PAGE} Скачивание чертежа'):
            calculation_number = self.get_calculation_number()
            expected_file_name = f'TDU{calculation_number}.zip'
            self.delete_file_by_name_in_download_folder(expected_file_name)
            self._btn_drawing.click(timeout=10.0)
            self.checking_the_download_document_in_the_download_folder(expected_file_name)
            self.delete_file_by_name_in_download_folder(expected_file_name)

    def click_download_drawing_production(self) -> None:
        """Клик по кнопке Чертёж в производство и проверка скачивания zip файла"""
        with allure.step(f'{self.NAME_PAGE} Скачивание чертежа в производство'):
            calculation_number = self.get_calculation_number()
            expected_file_name = f'TDU{calculation_number}.zip'
            self.delete_file_by_name_in_download_folder(expected_file_name)
            self._btn_drawing_production.click(timeout=10.0)
            self.checking_the_download_document_in_the_download_folder(expected_file_name)
            self.delete_file_by_name_in_download_folder(expected_file_name)

    def click_download_bom(self) -> None:
        """Клик по кнопке BOM и проверка скачивания xlsx файла"""
        with allure.step(f'{self.NAME_PAGE} Скачивание BOM'):
            calculation_number = self.get_calculation_number()
            expected_file_name = f'TDU{calculation_number}.xlsx'
            self.delete_file_by_name_in_download_folder(expected_file_name)
            self._btn_bom.click(timeout=10.0)
            self.checking_the_download_document_in_the_download_folder(expected_file_name)
            self.delete_file_by_name_in_download_folder(expected_file_name)