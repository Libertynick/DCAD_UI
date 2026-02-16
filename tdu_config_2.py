import allure
from selenium.webdriver.chrome.webdriver import WebDriver

from base_page.base_page import BasePage

from dcad_pages.tdu_config_2_page.tdu_filter_component import TduFilterComponent
from dcad_pages.tdu_config_2_page.tdu_results_component import TduResultsTableComponent

from elements.text import Text
from tools.routes.dcad_routes import DcadRoutes


class TduListPage(BasePage):
    """
    Страница Конфигуратор TDU - Список стандартных моделей (Config2)
    Содержит форму фильтров и таблицу результатов
    """

    def __init__(self, driver: WebDriver, url: str = DcadRoutes.PAGE_CONFIG_2):
        super().__init__(driver, url)

        # Components
        self.filter_component = TduFilterComponent(driver)
        self.results_table_component = TduResultsTableComponent(driver)

        # Text
        self._header_configurator_tdu = Text(
            driver,
            "//strong[text()='Конфигуратор TDU']","Описание страницы"
        )

    def should_header_page_visible(self) -> None:
        """Проверка отображения заголовка страницы"""
        with allure.step('Проверка отображения заголовка страницы "Конфигуратор TDU"'):
            self._header_configurator_tdu.wait_visible_on_page()