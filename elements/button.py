import allure

from elements.base_element import BaseElement


class Button(BaseElement):
    """
    Класс для работы с кнопками на странице. Наследует базовые методы от BaseElement и добавляет
    специфичные методы для работы с кнопками.
    """

    @property
    def type_of(self) -> str:
        """
        Возвращает тип элемента - button
        """
        return 'Кнопка'

    def check_enabled(self, index: int = 0, **kwargs):
        """Проверяем, что кнопка активна (enabled)"""
        with allure.step(f'Проверяем, что {self.type_of} {self.name} активна (enabled)'):
            element = self.find_element(index=index, **kwargs)
            is_enabled = element.is_enabled()
            assert is_enabled, f'Элемент {self.type_of} {self.name} не активна. is_enabled() - {is_enabled}'

    def check_disabled(self, index: int = 0, **kwargs):
        """Проверяем, что кнопка не активна (не доступна для клика)"""
        with (allure.step(f'Проверяем, что {self.type_of} {self.name} не активна (не доступна для клика)')):
            expected_attribute = 'disabled'
            is_disabled = self.get_attribute_by_name(index=index, name_attribute=expected_attribute, **kwargs)

            assert is_disabled == 'true', \
                f'Элемент "{self.type_of} {self.name}" активна (доступна для нажатия). Атрибут disabled - {is_disabled}'
