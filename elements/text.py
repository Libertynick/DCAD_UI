from elements.base_element import BaseElement


class Text(BaseElement):
    """
    Класс для работы с текстовыми элементами на странице.
    Наследует все основные методы от BaseElement
    """

    @property
    def type_of(self):
        """
        Возвращает тип элемента - элемент с текстом
        """
        return 'Текстовый элемент'
