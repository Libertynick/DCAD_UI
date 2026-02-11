from pathlib import Path

import allure
from selenium.webdriver.chrome.webdriver import WebDriver

from components.base_component import BaseComponent
from components.open_components.loader_component import LoaderComponent
from base_page.base_page import BasePage

from elements.button import Button
from elements.text import Text
from tools.validators import assertions


class TduResultsTableComponent(BaseComponent):
    """
    Компонент Таблица результатов на странице списка TDU
    Содержит колонки: Название, Клапан-партнёр, Артикул, Цена с НДС, Чертёж, Модификация
    Скриншот компонента: docs/images_component_dcad/tdu_list_page/tdu_results_table_component.png
    """

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

        self._loader_component = LoaderComponent(driver)
        self._base_page = BasePage(driver)

        # ===== TABLE HEADER =====

        self._table_title = Text(
            driver,
            "//small[text()='Список стандартных моделей узлов TDU']",
            "Заголовок таблицы 'Список стандартных моделей узлов TDU'"
        )

        # ===== TABLE COLUMNS =====

        self._column_name_header = Text(
            driver,
            "//th[text()='Название']",
            "Заголовок колонки 'Название'"
        )

        self._column_partner_valve_header = Text(
            driver,
            "//th[text()='Клапан-партнёр']",
            "Заголовок колонки 'Клапан-партнёр'"
        )

        self._column_article_header = Text(
            driver,
            "//th[text()='Артикул']",
            "Заголовок колонки 'Артикул'"
        )

        self._column_price_header = Text(
            driver,
            "//th[text()='Цена с НДС']",
            "Заголовок колонки 'Цена с НДС'"
        )

        self._column_drawing_header = Text(
            driver,
            "//th[text()='Чертёж']",
            "Заголовок колонки 'Чертёж'"
        )

        self._column_modification_header = Text(
            driver,
            "//th[text()='Модификация']",
            "Заголовок колонки 'Модификация'"
        )

        # ===== TABLE ROWS DATA =====

        # Все строки таблицы с результатами
        self._table_rows = Text(
            driver,
            "//tbody[@data-bind='foreach: tduListFiltered']//tr",
            "Строки таблицы с результатами"
        )

        # Название конфигурации по строке
        # Параметр {row_index} - номер строки (начиная с 1)
        self._name_by_row = Text(
            driver,
            "//tbody[@data-bind='foreach: tduListFiltered']//tr[{row_index}]//td[1]",
            "Название конфигурации в строке"
        )

        # Клапан-партнёр по строке
        self._partner_valve_by_row = Text(
            driver,
            "//tbody[@data-bind='foreach: tduListFiltered']//tr[{row_index}]//td[2]",
            "Клапан-партнёр в строке"
        )

        # Артикул по строке
        self._article_by_row = Text(
            driver,
            "//tbody[@data-bind='foreach: tduListFiltered']//tr[{row_index}]//td[3]",
            "Артикул в строке"
        )

        # Цена с НДС по строке
        self._price_by_row = Text(
            driver,
            "//tbody[@data-bind='foreach: tduListFiltered']//tr[{row_index}]//td[4]",
            "Цена с НДС в строке"
        )

        # ===== ACTION BUTTONS =====

        # Кнопка "Чертёж" по строке
        # Параметр {row_index} - номер строки
        self._btn_drawing_by_row = Button(
            driver,
            "//tbody[@data-bind='foreach: tduListFiltered']//tr[{row_index}]//a[contains(text(), 'Чертёж')]",
            "Кнопка 'Чертёж' в строке таблицы"
        )

        # Кнопка "Изменить" по строке
        # Параметр {row_index} - номер строки
        self._btn_modify_by_row = Button(
            driver,
            "//tbody[@data-bind='foreach: tduListFiltered']//tr[{row_index}]//a[contains(text(), 'Изменить')]",
            "Кнопка 'Изменить' в строке таблицы"
        )

        # Кнопка "Чертёж" по артикулу
        # Параметр {article} - артикул товара
        self._btn_drawing_by_article = Button(
            driver,
            "//a[text()='{article}']/ancestor::tr//a[contains(text(), 'Чертёж')]",
            "Кнопка 'Чертёж' по артикулу"
        )

        # Кнопка "Изменить" по артикулу
        self._btn_modify_by_article = Button(
            driver,
            "//a[text()='{article}']/ancestor::tr//a[contains(text(), 'Изменить')]",
            "Кнопка 'Изменить' по артикулу"
        )

    def should_table_title_visible(self) -> None:
        """Проверка отображения заголовка таблицы"""
        with allure.step('Проверка отображения заголовка таблицы результатов'):
            self._table_title.wait_visible_on_page()

    def get_table_rows_count(self) -> int:
        """
        Получение количества строк в таблице результатов
        :return: Количество строк
        """
        with allure.step('Получение количества строк в таблице'):
            rows = self._table_rows.find_elements_safely()
            return len(rows)

    def get_name_by_row(self, row_index: int) -> str:
        """
        Получение названия конфигурации по номеру строки
        :param row_index: Номер строки (начиная с 1)
        :return: Название конфигурации
        """
        with allure.step(f'Получение названия конфигурации из строки {row_index}'):
            return self._name_by_row.get_text_element(row_index=row_index)

    def get_article_by_row(self, row_index: int) -> str:
        """
        Получение артикула по номеру строки
        :param row_index: Номер строки (начиная с 1)
        :return: Артикул
        """
        with allure.step(f'Получение артикула из строки {row_index}'):
            return self._article_by_row.get_text_element(row_index=row_index)

    def get_price_by_row(self, row_index: int) -> float:
        """
        Получение цены с НДС по номеру строки
        :param row_index: Номер строки (начиная с 1)
        :return: Цена с НДС
        """
        with allure.step(f'Получение цены с НДС из строки {row_index}'):
            return self._price_by_row.get_float_value_from_line(row_index=row_index)

    def get_partner_valve_by_row(self, row_index: int) -> str:
        """
        Получение клапана-партнёра по номеру строки
        :param row_index: Номер строки (начиная с 1)
        :return: Клапан-партнёр
        """
        with allure.step(f'Получение клапана-партнёра из строки {row_index}'):
            return self._partner_valve_by_row.get_text_element(row_index=row_index)

    def download_drawing_by_row(self, row_index: int, expected_file_prefix: str = None) -> None:
        """
        Скачивание чертежа по номеру строки
        :param row_index: Номер строки (начиная с 1)
        :param expected_file_prefix: Ожидаемое начало имени файла (например: 'TDU.7R')
        """
        with allure.step(f'Скачивание чертежа из строки {row_index}'):
            # Удаляем предыдущие файлы .zip из папки загрузок
            downloads_path = self._base_page.search_for_the_last_downloaded_file_in_a_folder(
                str(Path.home() / "Downloads")
            )
            if downloads_path and downloads_path.endswith('.zip'):
                self._base_page.delete_file_by_name_in_download_folder(downloads_path)

            # Кликаем по кнопке "Чертёж"
            self._btn_drawing_by_row.click(row_index=row_index)

            # Проверяем скачивание файла
            if expected_file_prefix:
                self._base_page.checking_the_download_document_in_the_download_folder(
                    name_file=f'{expected_file_prefix}.zip',
                    time_load=10
                )

    def download_drawing_by_article(self, article: str) -> None:
        """
        Скачивание чертежа по артикулу
        :param article: Артикул товара
        """
        with allure.step(f'Скачивание чертежа для артикула {article}'):
            self._btn_drawing_by_article.click(article=article)

    def click_modify_by_row(self, row_index: int) -> None:
        """
        Клик по кнопке "Изменить" по номеру строки
        Открывает страницу редактора конфигурации TDU
        :param row_index: Номер строки (начиная с 1)
        """
        with allure.step(f'Клик по кнопке "Изменить" в строке {row_index}'):
            self._btn_modify_by_row.click(row_index=row_index)

    def click_modify_by_article(self, article: str) -> None:
        """
        Клик по кнопке "Изменить" по артикулу
        Открывает страницу редактора конфигурации TDU
        :param article: Артикул товара
        """
        with allure.step(f'Клик по кнопке "Изменить" для артикула {article}'):
            self._btn_modify_by_article.click(article=article)

    def get_all_articles_from_table(self) -> list[str]:
        """
        Получение всех артикулов из таблицы результатов
        :return: Список артикулов
        """
        with allure.step('Получение всех артикулов из таблицы результатов'):
            rows_count = self.get_table_rows_count()
            articles = []
            for i in range(1, rows_count + 1):
                article = self.get_article_by_row(i)
                articles.append(article)
            return articles

    def check_table_contains_article(self, expected_article: str) -> None:
        """
        Проверка наличия артикула в таблице результатов
        :param expected_article: Ожидаемый артикул
        """
        with allure.step(f'Проверка наличия артикула {expected_article} в таблице'):
            articles = self.get_all_articles_from_table()
            assertions.assert_contains(
                actual_value=articles,
                expected_contains=expected_article,
                allure_title='Проверка наличия артикула в таблице результатов',
                error_message=f'Артикул {expected_article} не найден в таблице. '
                              f'Доступные артикулы: {articles}'
            )

    def check_results_count(self, expected_count: int) -> None:
        """
        Проверка количества результатов в таблице
        :param expected_count: Ожидаемое количество строк
        """
        with allure.step(f'Проверка количества результатов в таблице: {expected_count}'):
            actual_count = self.get_table_rows_count()
            assertions.assert_eq(
                actual_value=actual_count,
                expected_value=expected_count,
                allure_title='Проверка количества строк в таблице результатов',
                error_message=f'Количество строк в таблице не соответствует ожидаемому. '
                              f'Фактическое: {actual_count}, ожидаемое: {expected_count}'
            )