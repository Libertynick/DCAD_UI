from selenium.webdriver.chrome.webdriver import WebDriver

from components.base_component import BaseComponent
from elements.button import Button

class HeaderDcadComponent(BaseComponent):
    """
    Шапка сайта DCAD
    """
    NAME_PAGE = "|Шапка сайта DCAD|"

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

        # Button
        self._btn_configurator_tdu = Button(
            driver,
            "//a[text()='Конфигуратор TDU']",
            "Конфигуратор TDU"
        )
