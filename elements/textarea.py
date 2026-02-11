from typing import Any

import allure

from elements.base_element import BaseElement
from tools.validators import assertions


class Textarea(BaseElement):
    """
    Класс для работы с многострочными текстовыми полями ввода на странице.
    Наследует все основные методы от BaseElement.
    """

    @property
    def type_of(self):
        """Возвращает тип элемента - элемент Многострочное поле ввода"""
        return 'Многострочное поле ввода'

    def get_value(self, index: int = 0, **kwargs) -> str:
        """Получение атрибута value"""
        with allure.step(f'Получение атрибута value у "{self.type_of} {self.name}"'):
            input_element = self.find_element(index=index, **kwargs)
            value = input_element.get_attribute('value')
            return value

    def clear_textarea(self, index: int = 0, **kwargs) -> None:
        """Очистка поля"""
        with allure.step(f'Очистка {self.type_of} "{self.name}"'):
            textarea = self.find_element(index=index, **kwargs)
            textarea.clear()

    def filling_textarea(self, text_to_fill: Any, index: int = 0, timeout: float = 5.0, **kwargs):
        """
        Заполнение поля textarea
        :param text_to_fill: Текст для заполнения
        :param index: Индекс элемента
        :param timeout: Время ожидания элемента для поиска
        :param kwargs: Аргументы для форматирования локатора
        """
        with allure.step(f'Заполнение поля "{self.type_of} {self.name}" значением ({text_to_fill})'):
            textarea = self.find_element(index=index, timeout=timeout, **kwargs)
            textarea.send_keys(text_to_fill)

    def should_value_in_textarea(self, expected_value: Any, index: int = 0, **kwargs):
        """
        Должно быть заданное значение в поле ввода типа textarea
        :param expected_value: Ожидаемое значение
        :param index: Индекс элемента
        :param kwargs: Аргументы для локатора
        """
        with (allure.step(
                f'Должно быть заданное значение - ({expected_value}) в поле ввода "{self.type_of} {self.name}"')):
            value_textarea = self.get_attribute_by_name(index=index, name_attribute='value', **kwargs).strip()
            expected_value = str(expected_value).strip()

            assertions.assert_eq(
                actual_value=value_textarea,
                expected_value=expected_value,
                allure_title='Сверяем значения на равенство',
                error_message=f'В "{self.type_of} {self.name}" значение - ({value_textarea}) '
                              f'не соответствует ожидаемому - ({expected_value})'
            )
