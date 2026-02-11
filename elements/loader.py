from elements.base_element import BaseElement


class Loader(BaseElement):
    """
    Лоадер
    Наследует все основные методы от BaseElement
    """

    @property
    def type_of(self):
        """
        Возвращает тип элемента - лоадер
        """
        return 'loader'
