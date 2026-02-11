import allure

from elements.base_element import BaseElement


class Li(BaseElement):
    """
    Элементы в выпадающем списке
    """

    @property
    def type_of(self):
        """Возвращает тип элемента - Элементы в выпадающем списке"""
        return 'Элемент в выпадающем списке'

    def should_elements_alphabetical(self, **kwargs):
        """
        Элементы должны быть по алфавиту
        :param kwargs: Аргументы для форматирования локатора
        """
        with (allure.step(f'Проверяем, что "{self.type_of} {self.name}" идут по алфавиту')):
            element_in_ul = self.get_text_list_element(**kwargs)
            sorted_list_element = sorted(element_in_ul, key=lambda x: (x != 'Все', x))  # Слово Все всегда вначале списка

            assert sorted_list_element == element_in_ul, \
                f'Элементы в выпадающем списке "{self.name}" идут не по алфавиту.'
