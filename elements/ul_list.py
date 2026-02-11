import allure

from elements.base_element import BaseElement


class UlList(BaseElement):
    """
    Класс для работы с выпадающими списками на странице.
    Наследует все основные методы от BaseElement, предоставляя возможность
    работать с выпадающими списками как элементами на странице
    """

    @property
    def type_of(self):
        """Возвращает тип элемента - Выпадающий список"""
        return 'Выпадающий список'

    def should_value_in_ul(self, expected_values_in_ul: list, **kwargs):
        """Должны быть определенные значения в выпадающем списке"""
        with (allure.step(f'Проверка, что "{self.name}" соответствуют ожидаемым - ({expected_values_in_ul})')):
            expected_values_in_ul = sorted(expected_values_in_ul)
            values_ul = sorted(self.get_text_list_element(**kwargs))

            assert values_ul == expected_values_in_ul, \
                f'"{self.name}" - ({values_ul}) не соответствуют ожидаемым - ({expected_values_in_ul})'
