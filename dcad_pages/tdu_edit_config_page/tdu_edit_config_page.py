from selenium.webdriver.chrome.webdriver import WebDriver
from base_page.base_page import BasePage
from elements.input import Input


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