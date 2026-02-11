import allure
from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver

from base_page.raise_exceptions import MyTimeoutException
from components.base_component import BaseComponent
from elements.loader import Loader


class LoaderDcadComponent(BaseComponent):
    """
      Компонент Лоадер DCAD страницы
    """

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

        self._loader_after_price = Loader(
            driver,
            "//div[@data-bind='visible: IsCalculating' and @class='form-group row align-items-center justify-content-md-center mt-2']//span[@class='spinner-grow spinner-grow-sm']",
            "Лоадер в DCAD при нажатии не кнопку Цена в редакторе конфигурации TDU")

    def waiting_for_loader_no_text_processing_on_page(self, timeout: int = 60):
        """Ожидание отработки лоадера после нажатия на кнопку Цена. Ожидает невидимость на странице"""
        with allure.step(f'Ожидание отработки лоадера без текста. Максимальное время ожидания - {timeout}'):
            step_time = 5
            time_wait = 0

            loader = len(self._loader_after_price.find_elements_safely())

            while loader > 0:
                try:
                    self._loader_after_price.wait_no_visible_on_page(timeout=step_time)
                except TimeoutException:
                    loader = len(self._loader_after_price.find_elements_safely())
                    time_wait += step_time
                    if time_wait >= timeout:
                        raise MyTimeoutException(f'Лоадер виден на странице. Время ожидания {timeout}')
                    continue

                loader = len(self._loader_after_price.find_elements_safely())