import allure

from elements.base_element import BaseElement
from tools.validators import assertions


class Link(BaseElement):
    """
    Класс для работы со ссылками на странице.
    Наследует все основные методы от BaseElement
    """

    @property
    def type_of(self):
        """
        Возвращает тип элемента - ссылка
        """
        return 'Ссылка'

    def should_href(self, expected_href: str, index: int = 0, **kwargs) -> None:
        """
        Проверка атрибута href у ссылки
        :param expected_href: Ожидаемый атрибут href
        :param index: Индекс найденного элемента
        :param kwargs: Аргументы локатора
        """
        with allure.step(f'Проверка атрибута href у "{self.type_of} {self.name}"'):
            href = self.get_attribute_by_name(name_attribute='href', index=index, **kwargs)

            assertions.assert_eq(
                actual_value=href,
                expected_value=expected_href,
                allure_title='Сверяем значения атрибутов href',
                error_message=f'Значение атрибута href у "{self.type_of} {self.name}" не соответствует ожидаемому. '
                              f'У элемента- {href}; ожидаемое- {expected_href}'
            )
