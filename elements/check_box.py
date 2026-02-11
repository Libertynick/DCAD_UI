import allure

from elements.base_element import BaseElement


class CheckBox(BaseElement):
    """
    Класс для работы с элементами типа check-box
    """

    @property
    def type_of(self):
        """Возвращает тип элемента - check-box"""
        return 'check-box'

    def should_check_box_not_selected(self, index: int = 0, **kwargs):
        """Чек-бокс должен быть не выбран"""
        with allure.step(f'Проверяем, что {self.type_of} {self.name} не выбран'):
            element = self.find_element(index=index, **kwargs)
            is_selected = element.is_selected()
            assert is_selected is False, f'{self.type_of} {self.name} выбран. is_selected - {is_selected}'

    def should_check_box_selected(self, index: int = 0, **kwargs):
        """Чек-бокс должен быть выбран"""
        with allure.step(f'Проверяем, что {self.type_of} {self.name} выбран'):
            element = self.find_element(index=index, **kwargs)
            is_selected = element.is_selected()
            assert is_selected is True, f'{self.type_of} {self.name} не выбран. is_selected - {is_selected}'

    def should_check_box_enabled(self, index: int = 0, **kwargs):
        """Чек бокс должен быть доступен для выбора"""
        with allure.step(f'Проверяем, что "{self.type_of} {self.name}" доступен для редактирования'):
            element = self.find_element(index=index, **kwargs)
            is_enabled = element.is_enabled()
            assert is_enabled is True, f'"{self.type_of} {self.name}" не доступен для редактирования. is_enabled - {is_enabled}'
