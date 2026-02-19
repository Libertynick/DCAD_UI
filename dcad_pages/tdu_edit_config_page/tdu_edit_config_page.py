import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from base_page.base_page import BasePage
from elements.input import Input
from tools.validators import assertions


class TduEditConfigPage(BasePage):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

        self._initial_config = Input(
            driver,
            "//input[@id = 'startConfig']",
            "Начальная конфигурация"
        )

    def get_initial_config_name(self) -> str:
        self._initial_config.wait_visible_on_page()
        return self._initial_config.get_value()

    def should_start_config_by_name_config(self, expected_start_config: str) -> None:
        """
        Должно быть определенное название в поле Начальная конфигурация
        :param expected_start_config: Ожидаемое название в поле Начальная конфигурация:
        """
        with allure.step(f'Проверка, что в поле Начальная конфигурация значение- {expected_start_config}'):
            name_on_page = self._initial_config.get_text_element()

            assertions.assert_eq(
                actual_value=name_on_page,
                expected_value=expected_start_config,
                allure_title='Проверяем значение в поле Начальная конфигурация',
                error_message=f'Значение в поле Начальная конфигурация не соответствует ожидаемому. '
                              f'На странице- {name_on_page}; ожидаемое- {expected_start_config}'
            )
