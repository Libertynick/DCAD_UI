import allure
from selenium.webdriver.chrome.webdriver import WebDriver

from base_page.base_page import BasePage
from components.base_component import BaseComponent
from elements.button import Button
from elements.text import Text


class TduEditModalComponent(BaseComponent):
    """
    Компонент модального окна результата расчёта TDU.
    Открывается при нажатии кнопки 'Создать расчёт'
    Содержит кнопку скачивания чертежа с id расчёта
    """

    NAME_PAGE = '|Модальное окно результата расчёта TDU|'

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

        self._base_page = BasePage(driver)

        # Text
        self._modal_title = Text(
            driver,
            "//h5[@id='staticBackdropLabel' and @class='modal-title' and text()='Новая конфигурация TDU']",
            "Заголовок модального окна"
        )
        self._calculation_id = Text(
            driver,
            "//button[@data-bind='click: LoadTDUDrawByCalculationId']//span[@data-bind='text:CalculationId']",
            "ID расчёта"
        )

        # Button
        self._btn_drawing = Button(
            driver,
            "//button[@data-bind='click: LoadTDUDrawByCalculationId']",
            "Кнопка Чертёж"
        )

    def should_modal_visible(self) -> None:
        with allure.step(f'{self.NAME_PAGE} Проверка отображения модального окна'):
            self._modal_title.wait_visible_on_page()

    def get_calculation_id(self) -> str:
        with allure.step(f'{self.NAME_PAGE} Получение ID расчёта'):
            self._calculation_id.wait_visible_on_page(timeout=10.0)
            return self._calculation_id.get_text_element()

    def click_download_drawing(self) -> None:
        """
        Клик по кнопке Чертёж и проверка скачивания zip файла.
        Имя файла формируется как TDU{calculation_id}.zip
        """
        with allure.step(f'{self.NAME_PAGE} Скачивание чертежа'):
            calculation_id = self.get_calculation_id()
            expected_file_name = f'TDU{calculation_id}.zip'

            self._base_page.delete_file_by_name_in_download_folder(expected_file_name)
            self._btn_drawing.click(timeout=10.0)
            self._base_page.checking_the_download_document_in_the_download_folder(expected_file_name)
            self._base_page.delete_file_by_name_in_download_folder(expected_file_name)