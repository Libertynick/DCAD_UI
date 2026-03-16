import allure
from selenium.webdriver.chrome.webdriver import WebDriver

from base_page.base_page import BasePage
from components.base_component import BaseComponent
from elements.button import Button
from elements.text import Text


class TduConfigModalComponent(BaseComponent):
    """
    Компонент модального окна результата конфигурации TDU.
    Открывается при нажатии кнопки 'Создать конфигурацию'.
    Содержит кнопки скачивания: Чертёж, Чертёж в производство, BOM.
    """

    NAME_PAGE = '|Модальное окно конфигурации TDU|'

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

        self._base_page = BasePage(driver)

        # Text
        self._modal_title = Text(
            driver,
            "//h5[@id='staticBackdropLabel']",
            "Заголовок модального окна"
        )
        self._calculation_id = Text(
            driver,
            "//span[@data-bind='text:CalculationId']",
            "ID расчёта"
        )

        # Button
        self._btn_drawing = Button(
            driver,
            "//button[@data-bind='click: LoadTDUDrawByCalculationId']",
            "Кнопка Чертёж"
        )
        self._btn_drawing_production = Button(
            driver,
            "//button[@data-bind='click: LoadTDUFactoryDrawByCalculationId']",
            "Кнопка Чертёж в производство"
        )
        self._btn_bom = Button(
            driver,
            "//div[@id='resultModal']//a[contains(.,'BOM')]",
            "Кнопка BOM"
        )

    def should_modal_visible(self) -> None:
        """Проверка отображения модального окна"""
        with allure.step(f'{self.NAME_PAGE} Проверка отображения модального окна'):
            self._modal_title.wait_visible_on_page()

    def get_calculation_id(self) -> str:
        """
        Получение ID расчёта из модального окна
        :return: ID расчёта
        """
        with allure.step(f'{self.NAME_PAGE} Получение ID расчёта'):
            self._calculation_id.wait_visible_on_page(timeout=10.0)
            return self._calculation_id.get_text_element()

    def click_download_drawing(self) -> None:
        """Клик по кнопке Чертёж и проверка скачивания zip файла"""
        with allure.step(f'{self.NAME_PAGE} Скачивание чертежа'):
            calculation_id = self.get_calculation_id()
            expected_file_name = f'TDU{calculation_id}.zip'
            self._base_page.delete_file_by_name_in_download_folder(expected_file_name)
            self._btn_drawing.click(timeout=10.0)
            self._base_page.checking_the_download_document_in_the_download_folder(expected_file_name)
            self._base_page.delete_file_by_name_in_download_folder(expected_file_name)

    def click_download_drawing_production(self) -> None:
        """Клик по кнопке Чертёж в производство и проверка скачивания zip файла"""
        with allure.step(f'{self.NAME_PAGE} Скачивание чертежа в производство'):
            calculation_id = self.get_calculation_id()
            expected_file_name = f'TDU{calculation_id}.zip'
            self._base_page.delete_file_by_name_in_download_folder(expected_file_name)
            self._btn_drawing_production.click(timeout=10.0)
            self._base_page.checking_the_download_document_in_the_download_folder(expected_file_name)
            self._base_page.delete_file_by_name_in_download_folder(expected_file_name)

    def click_download_bom(self) -> None:
        """Клик по кнопке BOM и проверка скачивания xlsx файла"""
        with allure.step(f'{self.NAME_PAGE} Скачивание BOM'):
            calculation_id = self.get_calculation_id()
            expected_file_name = f'TDU{calculation_id}.xlsx'
            self._base_page.delete_file_by_name_in_download_folder(expected_file_name)
            self._btn_bom.click(timeout=10.0)
            self._base_page.checking_the_download_document_in_the_download_folder(expected_file_name)
            self._base_page.delete_file_by_name_in_download_folder(expected_file_name)