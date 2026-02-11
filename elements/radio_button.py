import allure

from elements.base_element import BaseElement


class RadioButton(BaseElement):
    """
    Переключатель типа radio button
    """

    @property
    def type_of(self):
        """
        Возвращает тип элемента - Переключатель типа radio button
        """
        return 'Переключатель типа radio button'

    def is_selected_radio_button(self, index: int = 0, **kwargs):
        """Получить значение Выбран (true) или Не выбран (false)"""
        with allure.step(f'"{self.type_of} {self.name}" - получаем выбран или не выбран.'):
            radio_button = self.find_element(index=index, **kwargs)
            is_selected = radio_button.is_selected()
            return is_selected

    def radio_button_should_not_selected(self, index: int = 0):
        """Переключатель типа radio button должен быть не выбран"""
        with allure.step(f'Проверка, что "{self.type_of} {self.name}" не выбран'):
            is_selected = self.is_selected_radio_button(index=index)
            assert is_selected is False, f'{self.type_of} {self.name} выбран. is_selected - {is_selected}'

    def radio_button_should_selected(self, index: int = 0, **kwargs):
        """Переключатель типа radio button должен быть выбран"""
        with allure.step(f'Проверка, что "{self.type_of} {self.name}" выбран'):
            is_selected = self.is_selected_radio_button(index=index, **kwargs)
            assert is_selected is True, f'{self.type_of} {self.name} не выбран. is_selected - {is_selected}'
