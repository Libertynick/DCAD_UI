import re
from typing import Any

import allure

from elements.base_element import BaseElement
from tools.validators import assertions


class Input(BaseElement):
    """
    Класс для работы с полями ввода на странице типа input. Наследует базовые методы от BaseElement и добавляет
    специфичные методы для работы с полями ввода.
    """

    @property
    def type_of(self) -> str:
        """
        Возвращает тип элемента - input
        """
        return 'Поле ввода input'

    def filling_input(self, text_to_fill: Any, index: int = 0, timeout: float = 5.0, **kwargs):
        """
        Заполнение поля input
        :param text_to_fill: Текст для заполнения
        :param index: Индекс элемента
        :param timeout: Время ожидания элемента для поиска
        :param kwargs: Аргументы для форматирования локатора
        """
        with allure.step(f'Заполнение поля "{self.type_of} {self.name}" значением ({text_to_fill})'):
            input_element = self.find_element(index=index, timeout=timeout, **kwargs)
            input_element.send_keys(text_to_fill)

    def should_value_in_input_field(self, expected_value: Any, index: int = 0, **kwargs):
        """
        Должно быть заданное значение в поле ввода типа input
        :param expected_value: Ожидаемое значение
        :param index: Индекс элемента
        :param kwargs: Аргументы для локатора
        """
        with (allure.step(
                f'Должно быть заданное значение - ({expected_value}) в поле ввода "{self.type_of} {self.name}"')):
            value_input_element = self.get_attribute_by_name(index=index, name_attribute='value', **kwargs).strip()
            expected_value = str(expected_value).strip()

            assertions.assert_eq(
                actual_value=value_input_element,
                expected_value=expected_value,
                allure_title='Сверяем значения на равенство',
                error_message=f'В "{self.type_of} {self.name}" значение - ({value_input_element}) '
                              f'не соответствует ожидаемому - ({expected_value})'
            )

    def should_contains_value_in_input_field(self, expected_value: Any, index: int = 0, **kwargs):
        """
        Должно быть частичное значение в поле ввода типа input
        :param expected_value: Ожидаемое значение
        :param index: Индекс элемента
        :param kwargs: Аргументы для локатора
        """
        with (allure.step(
                f'Должно быть частичное значение - ({expected_value}) в поле ввода "{self.type_of} {self.name}"')):
            value_input_element = self.get_attribute_by_name(index=index, name_attribute='value', **kwargs)
            expected_value = str(expected_value)

            assertions.assert_contains(
                actual_value=value_input_element,
                expected_contains=expected_value,
                allure_title='Сравниваем значения',
                error_message=f'Ожидаемое значение - ({expected_value}) '
                              f'не присутствует в "{self.type_of} {self.name}" - ({value_input_element})'
            )

    def clear_input(self, index: int = 0, **kwargs):
        """Очистка поля input"""
        with allure.step(f'Очистка "{self.type_of} {self.name}"'):
            input_element = self.find_element(index=index, **kwargs)
            input_element.clear()

    def get_value(self, index: int = 0, **kwargs) -> str:
        """Получение атрибута value"""
        with allure.step(f'Получение атрибута value у "{self.type_of} {self.name}"'):
            input_element = self.find_element(index=index, **kwargs)
            value = input_element.get_attribute('value')
            return value

    def get_float_value_from_input(self, index: int = 0, **kwargs) -> float:
        """Получение числового значения float атрибута value"""
        with allure.step(f'Получение числового значения float атрибута value у "{self.type_of} {self.name}"'):
            input_element = self.find_element(index=index, **kwargs)
            value = input_element.get_attribute('value')
            value = re.sub(r'[^\d,.]', '', value)  # Оставляем только цифры и запятую
            value = value.replace(',', '.')
            return float(value)

    def get_value_list_input(self, **kwargs) -> list:
        """
        Получение атрибута value из списка input (в случае когда по одному локатору - несколько элементов)
        :param kwargs: Аргументы для форматирования локатора
        """
        with allure.step(f'Получение атрибута value из списка input "{self.type_of} {self.name}"'):
            input_elements = self.find_elements(**kwargs)
            values = [el.get_attribute('value') for el in input_elements]
            return values

    def should_is_not_editable(self, index: int = 0, **kwargs):
        """Должно быть не редактируемо"""
        with allure.step(f'"{self.type_of} {self.name}" не редактируемо'):
            input_element = self.find_element(index=index, **kwargs)
            is_editable = input_element.get_attribute('disabled')
            assert is_editable == 'true', f'"{self.type_of} {self.name}" редактируемо. disabled - {is_editable}'

    def should_is_not_editable_list_input(self, **kwargs):
        """Список полей ввода должны быть не редактируемы"""
        with (allure.step(f'Список полей "{self.type_of} {self.name}" не редактируем')):
            input_element_list = self.find_elements(**kwargs)

            count = 1
            for el in input_element_list:
                is_editable = el.get_attribute('disabled')
                assert is_editable == 'true', \
                    f'"{self.type_of} {self.name} по счету номер {count}" редактируемо. disabled - {is_editable}'
                count += 1

    def should_placeholder(self, expected_placeholder: str, index: int = 0, **kwargs):
        """
        Должен быть определенный placeholder
        :param expected_placeholder: Ожидаемая подсказка
        :param index: Индекс элемента
        :param kwargs: Аргументы для форматирования локатора
        """
        with (allure.step(f'Проверка, что есть подсказка для ввода в "{self.type_of} {self.name}"')):
            input_element = self.find_element(index=index, **kwargs)
            placeholder = input_element.get_attribute('placeholder')
            assert expected_placeholder == placeholder, \
                f'Подсказка в {self.type_of} {self.name} - ({placeholder}) не соответствует ожидаемой - ({expected_placeholder})'

    def check_is_selected(self, index: int = 0, **kwargs):
        """Проверяем, что кнопка выбрана. В основном подходит для <input type="radio">"""
        with allure.step(f'Проверяем, что {self.type_of} {self.name} выбрана'):
            element = self.find_element(index=index, **kwargs)
            is_selected = element.is_selected()
            assert is_selected is True, f'{self.type_of} {self.name} не выбрана. is_selected - {is_selected}'
