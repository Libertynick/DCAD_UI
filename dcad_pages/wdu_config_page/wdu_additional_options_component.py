import allure
from selenium.webdriver.chrome.webdriver import WebDriver

from components.base_component import BaseComponent
from elements.button import Button
from elements.check_box import CheckBox
from elements.options import Options
from tools.validators import assertions


class WduAdditionalOptionsComponent(BaseComponent):
    """
    Компонент Дополнительные опции на странице Конфигуратор ВДУ
    Содержит 4 селекта: Воздухоотводчик, Дренаж, Учет, КИП
    и 5 чекбоксов: Фильтр на вводе, Отводы вверх, Обр.клапан на каждый отвод,
    Доп.фильтр на каждый отвод, Доп.кран на каждый отвод
    """

    NAME_PAGE = '|Страница конфигуратор ВДУ|'

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

        # Options
        self._select_air_vent = Options(driver, "//select[@id='8']", "Воздухоотводчик")
        self._select_drainage = Options(driver, "//select[@id='9']", "Дренаж")
        self._select_accounting = Options(driver, "//select[@id='10']", "Учет")
        self._select_kip = Options(driver, "//select[@id='19']", "КИП")

        # CheckBox (input — для чтения состояния)
        self._cb_filter_inlet = CheckBox(driver, "//input[@id='12']", "Фильтр на вводе")
        self._cb_outlets_up = CheckBox(driver, "//input[@id='13']", "Отводы вверх")
        self._cb_return_valve = CheckBox(driver, "//input[@id='14']", "Обр.клапан на каждый отвод")
        self._cb_extra_filter = CheckBox(driver, "//input[@id='15']", "Доп.фильтр на каждый отвод")
        self._cb_extra_valve = CheckBox(driver, "//input[@id='16']", "Доп.кран на каждый отвод")

        # Button (label — для клика)
        self._btn_filter_inlet = Button(driver, "//label[@for='12']", "Фильтр на вводе (label)")
        self._btn_outlets_up = Button(driver, "//label[@for='13']", "Отводы вверх (label)")
        self._btn_return_valve = Button(driver, "//label[@for='14']", "Обр.клапан на каждый отвод (label)")
        self._btn_extra_filter = Button(driver, "//label[@for='15']", "Доп.фильтр на каждый отвод (label)")
        self._btn_extra_valve = Button(driver, "//label[@for='16']", "Доп.кран на каждый отвод (label)")

    def get_selected_air_vent(self) -> str:
        """
        Получение выбранного значения Воздухоотводчик
        :return: Текст выбранного значения
        """
        with allure.step(f'{self.NAME_PAGE} Получение выбранного Воздухоотводчика'):
            return self._select_air_vent.get_selected_text()

    def select_air_vent(self, value: str) -> None:
        """
        Выбор значения Воздухоотводчик
        :param value: Текст опции для выбора
        """
        with allure.step(f'{self.NAME_PAGE} Выбор Воздухоотводчика: {value}'):
            self._select_air_vent.select_option(value)
            assertions.assert_eq(
                actual_value=self.get_selected_air_vent(),
                expected_value=value,
                allure_title='Проверяем выбранный Воздухоотводчик',
                error_message='Несоответствие выбранного Воздухоотводчика'
            )

    def get_selected_drainage(self) -> str:
        """
        Получение выбранного значения Дренаж
        :return: Текст выбранного значения
        """
        with allure.step(f'{self.NAME_PAGE} Получение выбранного Дренажа'):
            return self._select_drainage.get_selected_text()

    def select_drainage(self, value: str) -> None:
        """
        Выбор значения Дренаж
        :param value: Текст опции для выбора
        """
        with allure.step(f'{self.NAME_PAGE} Выбор Дренажа: {value}'):
            self._select_drainage.select_option(value)
            assertions.assert_eq(
                actual_value=self.get_selected_drainage(),
                expected_value=value,
                allure_title='Проверяем выбранный Дренаж',
                error_message='Несоответствие выбранного Дренажа'
            )

    def get_selected_accounting(self) -> str:
        """
        Получение выбранного значения Учет
        :return: Текст выбранного значения
        """
        with allure.step(f'{self.NAME_PAGE} Получение выбранного Учета'):
            return self._select_accounting.get_selected_text()

    def select_accounting(self, value: str) -> None:
        """
        Выбор значения Учет
        :param value: Текст опции для выбора
        """
        with allure.step(f'{self.NAME_PAGE} Выбор Учета: {value}'):
            self._select_accounting.select_option(value)
            assertions.assert_eq(
                actual_value=self.get_selected_accounting(),
                expected_value=value,
                allure_title='Проверяем выбранный Учет',
                error_message='Несоответствие выбранного Учета'
            )

    def get_selected_kip(self) -> str:
        """
        Получение выбранного значения КИП
        :return: Текст выбранного значения
        """
        with allure.step(f'{self.NAME_PAGE} Получение выбранного КИП'):
            return self._select_kip.get_selected_text()

    def select_kip(self, value: str) -> None:
        """
        Выбор значения КИП
        :param value: Текст опции для выбора
        """
        with allure.step(f'{self.NAME_PAGE} Выбор КИП: {value}'):
            self._select_kip.select_option(value)
            assertions.assert_eq(
                actual_value=self.get_selected_kip(),
                expected_value=value,
                allure_title='Проверяем выбранный КИП',
                error_message='Несоответствие выбранного КИП'
            )

    def is_filter_inlet_checked(self) -> bool:
        """
        Получение состояния чекбокса Фильтр на вводе
        :return: True если чекбокс выбран
        """
        with allure.step(f'{self.NAME_PAGE} Получение состояния Фильтр на вводе'):
            return self._cb_filter_inlet.find_element().is_selected()

    def toggle_filter_inlet(self) -> None:
        """Переключение чекбокса Фильтр на вводе"""
        with allure.step(f'{self.NAME_PAGE} Переключение Фильтр на вводе'):
            self._btn_filter_inlet.click()

    def is_outlets_up_checked(self) -> bool:
        """
        Получение состояния чекбокса Отводы вверх
        :return: True если чекбокс выбран
        """
        with allure.step(f'{self.NAME_PAGE} Получение состояния Отводы вверх'):
            return self._cb_outlets_up.find_element().is_selected()

    def toggle_outlets_up(self) -> None:
        """Переключение чекбокса Отводы вверх"""
        with allure.step(f'{self.NAME_PAGE} Переключение Отводы вверх'):
            self._btn_outlets_up.click()

    def is_return_valve_checked(self) -> bool:
        """
        Получение состояния чекбокса Обр.клапан на каждый отвод
        :return: True если чекбокс выбран
        """
        with allure.step(f'{self.NAME_PAGE} Получение состояния Обр.клапан на каждый отвод'):
            return self._cb_return_valve.find_element().is_selected()

    def toggle_return_valve(self) -> None:
        """Переключение чекбокса Обр.клапан на каждый отвод"""
        with allure.step(f'{self.NAME_PAGE} Переключение Обр.клапан на каждый отвод'):
            self._btn_return_valve.click()

    def is_extra_filter_checked(self) -> bool:
        """
        Получение состояния чекбокса Доп.фильтр на каждый отвод
        :return: True если чекбокс выбран
        """
        with allure.step(f'{self.NAME_PAGE} Получение состояния Доп.фильтр на каждый отвод'):
            return self._cb_extra_filter.find_element().is_selected()

    def toggle_extra_filter(self) -> None:
        """Переключение чекбокса Доп.фильтр на каждый отвод"""
        with allure.step(f'{self.NAME_PAGE} Переключение Доп.фильтр на каждый отвод'):
            self._btn_extra_filter.click()

    def is_extra_valve_checked(self) -> bool:
        """
        Получение состояния чекбокса Доп.кран на каждый отвод
        :return: True если чекбокс выбран
        """
        with allure.step(f'{self.NAME_PAGE} Получение состояния Доп.кран на каждый отвод'):
            return self._cb_extra_valve.find_element().is_selected()

    def toggle_extra_valve(self) -> None:
        """Переключение чекбокса Доп.кран на каждый отвод"""
        with allure.step(f'{self.NAME_PAGE} Переключение Доп.кран на каждый отвод'):
            self._btn_extra_valve.click()

    def should_additional_params_match(self, params: dict) -> None:
        """
        Проверка что все дополнительные параметры соответствуют ожидаемым
        :param params: Словарь с ожидаемыми значениями
        """
        with allure.step(f'{self.NAME_PAGE} Проверка соответствия дополнительных параметров'):
            assertions.assert_eq(self.get_selected_air_vent(), params['air_vent'],
                                 allure_title='Воздухоотводчик', error_message='Несоответствие Воздухоотводчика')
            assertions.assert_eq(self.get_selected_drainage(), params['drainage'],
                                 allure_title='Дренаж', error_message='Несоответствие Дренажа')
            assertions.assert_eq(self.get_selected_accounting(), params['accounting'],
                                 allure_title='Учет', error_message='Несоответствие Учета')
            assertions.assert_eq(self.get_selected_kip(), params['kip'],
                                 allure_title='КИП', error_message='Несоответствие КИП')
            assertions.assert_eq(self.is_filter_inlet_checked(), params['filter_inlet'],
                                 allure_title='Фильтр на вводе', error_message='Несоответствие Фильтр на вводе')
            assertions.assert_eq(self.is_outlets_up_checked(), params['outlets_up'],
                                 allure_title='Отводы вверх', error_message='Несоответствие Отводы вверх')
            assertions.assert_eq(self.is_return_valve_checked(), params['return_valve'],
                                 allure_title='Обр.клапан', error_message='Несоответствие Обр.клапан')
            assertions.assert_eq(self.is_extra_filter_checked(), params['extra_filter'],
                                 allure_title='Доп.фильтр', error_message='Несоответствие Доп.фильтр')
            assertions.assert_eq(self.is_extra_valve_checked(), params['extra_valve'],
                                 allure_title='Доп.кран', error_message='Несоответствие Доп.кран')