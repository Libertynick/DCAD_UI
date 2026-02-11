from selenium.webdriver.chrome.webdriver import WebDriver


class BaseComponent:
    """
    Базовый компонент страницы.
    """

    def __init__(self, driver: WebDriver):
        self.driver = driver
