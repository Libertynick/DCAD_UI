import allure
from selenium.webdriver.support.ui import Select as SeleniumSelect

from elements.base_element import BaseElement


class Options(BaseElement):
    """
    Класс для работы с выпадающим списком select на странице. Наследует базовые методы от BaseElement и добавляет
    специфичные методы для работы с выпадающим списком select.
    """

    @property
    def type_of(self):
        """
        Возвращает тип элемента - выпадающий список select
        """
        return 'Элемент в выпадающем списке select'

    def select_option(self, text: str, index: int = 0, **kwargs):
        """Выбрать option по-видимому тексту
        :param text: текст для поиска элемента
        :param index: порядковый номер найденного элемента
        """
        with allure.step(f'Выбираем {self.type_of} {self.name} по тексту - {text}'):
            element = self.find_element(index=index, **kwargs)
            SeleniumSelect(element).select_by_visible_text(text)

    def get_selected_text(self, index: int = 0, **kwargs) -> str:
        """Получить текст выбранного option
        :return: текст элемента option
        """
        with allure.step(f'Получение текста из {self.type_of} {self.name}'):
            element = self.find_element(index=index, **kwargs)
            return SeleniumSelect(element).first_selected_option.text