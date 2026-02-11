import allure

from elements.base_element import BaseElement
from tools.validators import assertions


class Img(BaseElement):
    """Класс для работы с картинками на странице"""

    @property
    def type_of(self):
        """Возвращает тип элемента - изображение"""
        return 'Изображение'

    def should_src_img(self, expected_src: str, index: int = 0, **kwargs) -> None:
        """
        Должен быть определенный атрибут src у элемента
        :param expected_src: Ожидаемый атрибут src
        :param index: Индекс элемента
        """
        with allure.step(f'Проверка атрибута src у "{self.type_of} {self.name}"'):
            src = self.get_attribute_by_name(name_attribute='src', index=index, **kwargs)

            assertions.assert_eq(
                actual_value=src,
                expected_value=expected_src,
                allure_title='Сверяем значения атрибутов src',
                error_message=f'Значение атрибута src у "{self.type_of} {self.name}" не соответствует ожидаемому. '
                              f'У элемента- {src}; ожидаемое- {expected_src}'
            )
