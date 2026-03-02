import allure
from selenium.webdriver.chrome.webdriver import WebDriver

from base_page.base_page import BasePage
from dcad_pages.tdu_edit_config_page.tdu_edit_modal_component import TduEditModalComponent
from elements.button import Button
from elements.check_box import CheckBox
from elements.input import Input
from elements.options import Options
from elements.text import Text
from tools.validators import assertions


class TduEditConfigPage(BasePage):
    """
    Страница изменения конфигурации TDU
    """

    NAME_PAGE = '|Страница редактирования конфигурации TDU|'

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

        self.result_modal = TduEditModalComponent(driver)

        # Input
        self._initial_config = Input(
            driver,
            "//input[@id='startConfig']",
            "Начальная конфигурация"
        )
        self._result_name = Input(
            driver,
            "//input[@id='autoName']",
            "Название после расчёта"
        )
        self._result_price = Input(
            driver,
            "//input[@id='pricePreview']",
            "Цена после расчёта"
        )

        # Button
        self._btn_price = Button(
            driver,
            "//button[text()='Цена']",
            "Цена"
        )
        self._btn_create_calculation = Button(
            driver,
            "//button[@data-bind='click: CreateCalculation']",
            "Кнопка Создать расчёт"
        )

        # Text
        self._canvas_draw = Text(
            driver,
            "//canvas[@id='draw']",
            "Схема конфигурации"
        )

        # Options
        self._select_inlet_diameter = Options(
            driver,
            "//select[@data-bind='value: inputBvDn']",
            "Диаметр вводной группы"
        )
        self._select_partner_valve = Options(
            driver,
            "//select[@aria-describedby='inputPartnerIdHelp']",
            "Клапан-партнёр"
        )

        # CheckBox
        self._checkbox_brackets = CheckBox(
            driver,
            "//label[@for='brackets' and contains(@class, 'custom-control-label')]",
            "Кронштейны"
        )

    def get_initial_config_name(self) -> str:
        with allure.step(f'{self.NAME_PAGE} Получение значения поля Начальная конфигурация'):
            return self._initial_config.get_value()

    def should_start_config_by_name_config(self, expected_start_config: str) -> None:
        with allure.step(f'{self.NAME_PAGE} Проверка, что в поле Начальная конфигурация значение- {expected_start_config}'):
            name_on_page = self._initial_config.get_value()
            assertions.assert_eq(
                actual_value=name_on_page,
                expected_value=expected_start_config,
                allure_title='Проверяем значение в поле Начальная конфигурация',
                error_message=f'На странице- {name_on_page}; ожидаемое- {expected_start_config}'
            )

    def click_price_button(self) -> None:
        """Клик по кнопке Цена и ожидание появления результата"""
        with allure.step(f'{self.NAME_PAGE} Клик по кнопке Цена и ожидание появления результата'):
            self._btn_price.click(timeout=5.0)
            self._result_name.wait_visible_on_page(timeout=15.0)
            self._result_name.scroll_to_elem_js()

    def get_result_name(self) -> str:
        with allure.step(f'{self.NAME_PAGE} Получение названия из результата расчёта'):
            return self._result_name.get_value()

    def get_result_price(self) -> float:
        with allure.step(f'{self.NAME_PAGE} Получение цены из результата расчёта'):
            return self._result_price.get_float_value_from_input()

    def should_result_name_eq(self, expected_name: str) -> None:
        with allure.step(f'{self.NAME_PAGE} Проверка названия конфигурации после расчёта - {expected_name}'):
            actual_name = self.get_result_name()
            assertions.assert_eq(
                actual_value=actual_name,
                expected_value=expected_name,
                allure_title='Проверяем название конфигурации после расчёта',
                error_message=f'Название после расчёта не совпадает. '
                              f'На странице - {actual_name}; ожидаемое - {expected_name}'
            )

    def should_result_price_within_tolerance(self, expected_price: float, tolerance: float = 0.07) -> None:
        with allure.step(f'{self.NAME_PAGE} Проверка цены после расчёта. Ожидаемая - {expected_price}, допуск - {tolerance * 100}%'):
            actual_price = self.get_result_price()
            deviation = abs(actual_price - expected_price) / expected_price
            assertions.assert_less_than(
                actual_value=deviation,
                less_value=tolerance,
                allure_title='Проверяем отклонение цены от ожидаемой',
                error_message=f'Цена отличается более чем на {tolerance * 100}%. '
                              f'На странице - {actual_price}; в списке - {expected_price}; '
                              f'отклонение - {deviation * 100:.1f}%'
            )

    def should_canvas_visible(self) -> None:
        with allure.step(f'{self.NAME_PAGE} Проверка отображения схемы конфигурации'):
            self._canvas_draw.wait_visible_on_page()

    def click_create_calculation(self) -> None:
        with allure.step(f'{self.NAME_PAGE} Клик по кнопке Создать расчёт'):
            self._btn_create_calculation.click()
            self.result_modal.should_modal_visible()

    def select_inlet_diameter(self, value: str) -> None:
        with allure.step(f'{self.NAME_PAGE} Выбор диаметра вводной группы - {value}'):
            self._select_inlet_diameter.wait_visible_on_page(timeout=10.0)
            self._select_inlet_diameter.scroll_to_elem_js()
            self._select_inlet_diameter.select_option(value)
            selected = self._select_inlet_diameter.get_selected_text()
            assertions.assert_eq(
                actual_value=selected,
                expected_value=value,
                allure_title='Проверяем выбранный диаметр вводной группы',
                error_message=f'Несоответствие выбранного диаметра вводной группы. '
                              f'На странице - {selected}; ожидаемое - {value}'
            )

    def select_partner_valve(self, value: str) -> None:
        with allure.step(f'{self.NAME_PAGE} Выбор клапана-партнёра - {value}'):
            self._select_partner_valve.wait_visible_on_page(timeout=10.0)
            self._select_partner_valve.scroll_to_elem_js()
            self._select_partner_valve.select_option(value)
            selected = self._select_partner_valve.get_selected_text()
            assertions.assert_eq(
                actual_value=selected,
                expected_value=value,
                allure_title='Проверяем выбранный клапан-партнёр',
                error_message=f'Несоответствие выбранного клапана-партнёра. '
                              f'На странице - {selected}; ожидаемое - {value}'
            )

    def check_brackets(self) -> None:
        """Установить галку Кронштейны"""
        with allure.step(f'{self.NAME_PAGE} Установка галки Кронштейны'):
            self._checkbox_brackets.click()
            self._checkbox_brackets.should_check_box_selected()

    def uncheck_brackets(self) -> None:
        """Снять галку Кронштейны"""
        with allure.step(f'{self.NAME_PAGE} Снятие галки Кронштейны'):
            self._checkbox_brackets.click()
            self._checkbox_brackets.should_check_box_not_selected()

    def should_result_name_contains(self, expected_text: str) -> None:
        with allure.step(f'{self.NAME_PAGE} Проверка, что название после расчёта содержит - {expected_text}'):
            actual_name = self.get_result_name()
            assertions.assert_contains(
                actual_value=actual_name,
                expected_contains=expected_text,
                allure_title='Проверяем что название содержит ожидаемый текст',
                error_message=f'Название после расчёта не содержит ожидаемый текст. '
                              f'На странице - {actual_name}; ожидаемый текст - {expected_text}'
            )

    def should_result_price_changed(self, price_before: float) -> None:
        with allure.step(f'{self.NAME_PAGE} Проверка, что цена изменилась. Цена до - {price_before}'):
            actual_price = self.get_result_price()
            assertions.assert_not_eq(
                actual_value=actual_price,
                value_not_eq=price_before,
                allure_title='Проверяем что цена изменилась после смены параметра',
                error_message=f'Цена не изменилась после смены параметра. '
                              f'Цена до - {price_before}; цена после - {actual_price}'
            )