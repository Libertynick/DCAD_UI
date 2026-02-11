import allure
from selenium.webdriver.chrome.webdriver import WebDriver

from base_page.base_page import BasePage
from components.open_components.loader_component import LoaderComponent

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
            "//strong[text()='Конфигуратор TDU']",
            "Описание страницы"
        )

    def should_header_page_visible(self) -> None:
        """Проверка отображения заголовка страницы"""
        with allure.step('Проверка отображения заголовка страницы "Конфигуратор TDU"'):
            self._header_configurator_tdu.wait_visible_on_page()

    def search_tdu_by_filters(self, node_type: str = None, branches: str = None,
                              riser: str = None, inlet_diameter: str = None,
                              partner_valve: str = None, branch_valves: str = None) -> None:
        """
        Поиск конфигурации TDU по фильтрам
        :param node_type: Тип узла (например: 'TDU.7R', 'TDU.5R', 'TDU.3R')
        :param branches: Количество отводов (например: '2', '3', '4')
        :param riser: Стояк (например: 'Слева', 'Справа')
        :param inlet_diameter: Диаметр ввода (например: '20', '25', '32')
        :param partner_valve: Клапан-партнёр (например: 'Есть', 'Нет')
        :param branch_valves: Клапаны на отводах (например: 'MVT-R', 'MVT-R LF', 'MNT-R')
        """
        with allure.step('Поиск конфигурации TDU по фильтрам'):
            self.filter_component.set_filters(
                node_type=node_type,
                branches=branches,
                riser=riser,
                inlet_diameter=inlet_diameter,
                partner_valve=partner_valve,
                branch_valves=branch_valves
            )
            # После выбора фильтров таблица обновляется автоматически (без лоадера)
            self.results_table_component.should_table_title_visible()

    def download_drawing_by_article(self, article: str) -> None:
        """
        Скачивание чертежа по артикулу
        :param article: Артикул товара
        """
        with allure.step(f'Скачивание чертежа для артикула {article}'):
            self.results_table_component.download_drawing_by_article(article)

    def open_editor_by_article(self, article: str) -> None:
        """
        Открытие редактора конфигурации по артикулу (кнопка "Изменить")
        :param article: Артикул товара
        """
        with allure.step(f'Открытие редактора конфигурации для артикула {article}'):
            self.results_table_component.click_modify_by_article(article)

    def get_first_result_article(self) -> str:
        """
        Получение артикула первого результата в таблице
        :return: Артикул
        """
        with allure.step('Получение артикула первого результата'):
            return self.results_table_component.get_article_by_row(row_index=1)

    def verify_search_results_not_empty(self) -> None:
        """Проверка, что результаты поиска не пустые"""
        with allure.step('Проверка наличия результатов поиска'):
            rows_count = self.results_table_component.get_table_rows_count()
            assert rows_count > 0, 'Таблица результатов пуста'