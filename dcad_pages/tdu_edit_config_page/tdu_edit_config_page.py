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

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

        self.result_modal = TduEditModalComponent(driver)

        # Input
        self._initial_config = Input(
            driver,
            "//input[@id = 'startConfig']",
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
        """
        Должно быть определенное название в поле Начальная конфигурация
        :param expected_start_config: Ожидаемое название в поле Начальная конфигурация:
        """
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
        """Получение названия конфигурации из результата расчёта"""
        with allure.step(f'{self.NAME_PAGE} Получение названия из результата расчёта'):
            return self._result_name.get_value()

    def get_result_price(self) -> float:
        """Получение цены из результата расчёта"""
        with allure.step(f'{self.NAME_PAGE} Получение цены из результата расчёта'):
            return self._result_price.get_float_value_from_input()

    def should_result_name_eq(self, expected_name: str) -> None:
        """
        Название после расчёта должно совпадать с ожидаемым
        :param expected_name: Ожидаемое название конфигурации
        """
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
        """
        Цена после расчёта должна отличаться от ожидаемой не более чем на tolerance
        :param expected_price: Ожидаемая цена из Config2
        :param tolerance: Допустимое отклонение (по умолчанию 7%)
        """
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
        """Схема конфигурации должна отображаться"""
        with allure.step(f'{self.NAME_PAGE} Проверка отображения схемы конфигурации'):
            self._canvas_draw.wait_visible_on_page()

    def click_create_calculation(self) -> None:
        """Клик по кнопке Создать расчёт и ожидание открытия модального окна"""
        with allure.step(f'{self.NAME_PAGE} Клик по кнопке Создать расчёт'):
            self._btn_create_calculation.click()
            self.result_modal.should_modal_visible()

    def select_inlet_diameter(self, value: str) -> None:
        """
        Выбор диаметра вводной группы
        :param value: Значение диаметра для выбора
        """
        with allure.step(f'{self.NAME_PAGE} Выбор диаметра вводной группы - {value}'):
            self._select_inlet_diameter.select_option(value)
            self._select_inlet_diameter.should_text_in_element(expected_text=value)

    def select_partner_valve(self, value: str) -> None:
        """
        Выбор клапана-партнёра
        :param value: Значение клапана для выбора
        """
        with allure.step(f'{self.NAME_PAGE} Выбор клапана-партнёра - {value}'):
            self._select_partner_valve.select_option(value)
            # Проверить, что выбрано нужное значение

    def click_checkbox_brackets(self) -> None:
        """Клик по чекбоксу Кронштейны"""
        with allure.step(f'{self.NAME_PAGE} Клик по чекбоксу Кронштейны'):
            self._checkbox_brackets.click()
            # Проверить выбран ли чек-бокс. Разделить методы на выбор и на отмену выбора чек-бокса

    def should_result_name_contains(self, expected_text: str) -> None:
        """
        Название после расчёта должно содержать ожидаемый текст
        :param expected_text: Ожидаемый текст в названии конфигурации
        """
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
        """
        Цена после расчёта должна отличаться от переданной
        :param price_before: Цена до изменения параметра
        """
        with allure.step(f'{self.NAME_PAGE} Проверка, что цена изменилась. Цена до - {price_before}'):
            actual_price = self.get_result_price()

            assertions.assert_not_eq(
                actual_value=actual_price,
                value_not_eq=price_before,
                allure_title='Проверяем что цена изменилась после смены параметра',
                error_message=f'Цена не изменилась после смены параметра. '
                              f'Цена до - {price_before}; цена после - {actual_price}'
            )
