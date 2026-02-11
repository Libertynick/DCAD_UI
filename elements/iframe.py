import allure

from elements.base_element import BaseElement


class Iframe(BaseElement):
    """
    Класс для работы с элементами фрэйма
    """

    @property
    def type_of(self):
        """Возвращает тип элемента iframe"""
        return 'iframe'

    def switch_to_frame(self, index: int = 0, timeout: float = 5.0, **kwargs):
        """Переключение во фрэйм
        :param index: Индекс элемента
        :param timeout: Время ожидания элемента для поиска
        :param kwargs: Аргументы для форматирования локатора
        """
        with allure.step(f'Переключение в "{self.type_of} {self.name}"'):
            iframe = self.find_element(index=index, timeout=timeout, **kwargs)
            self.driver.switch_to.frame(iframe)
