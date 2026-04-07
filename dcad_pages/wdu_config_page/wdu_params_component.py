import allure
from selenium.webdriver.chrome.webdriver import WebDriver

from components.base_component import BaseComponent
from elements.options import Options
from tools.validators import assertions


class WduParamsComponent(BaseComponent):
    """
    Компонент Основные параметры на странице Конфигуратор ВДУ
    Содержит 7 селектов: Тип узла, Количество отводов, Подключение,
    Коллектор, Редуктор, Ду арматуры на отводах, Ду арматуры на вводе
    """

    NAME_PAGE = '|Страница конфигуратор ВДУ|'

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

        self._select_node_type = Options(driver, "//select[@id='1']", "Тип узла")
        self._select_branches = Options(driver, "//select[@id='2']", "Количество отводов")
        self._select_connection = Options(driver, "//select[@id='3']", "Подключение")
        self._select_collector = Options(driver, "//select[@id='5']", "Коллектор")
        self._select_reducer = Options(driver, "//select[@id='7']", "Редуктор")
        self._select_branch_dn = Options(driver, "//select[@id='6']", "Ду арматуры на отводах")
        self._select_inlet_dn = Options(driver, "//select[@id='4']", "Ду арматуры на вводе")

    def get_selected_node_type(self) -> str:
        """
        Получение выбранного типа узла
        :return: Текст выбранного значения
        """
        with allure.step(f'{self.NAME_PAGE} Получение выбранного типа узла'):
            return self._select_node_type.get_selected_text()

    def select_node_type(self, node_type: str) -> None:
        """
        Выбор типа узла
        :param node_type: Текст опции для выбора
        """
        with allure.step(f'{self.NAME_PAGE} Выбор типа узла: {node_type}'):
            self._select_node_type.click()
            self._select_node_type.select_option(node_type)
            assertions.assert_eq(
                actual_value=self.get_selected_node_type(),
                expected_value=node_type,
                allure_title='Проверяем выбранный тип узла',
                error_message=f'Несоответствие выбранного типа узла'
            )

    def get_selected_branches(self) -> str:
        """
        Получение выбранного количества отводов
        :return: Текст выбранного значения
        """
        with allure.step(f'{self.NAME_PAGE} Получение выбранного количества отводов'):
            return self._select_branches.get_selected_text()

    def select_branches(self, branches: str) -> None:
        """
        Выбор количества отводов
        :param branches: Текст опции для выбора
        """
        with allure.step(f'{self.NAME_PAGE} Выбор количества отводов: {branches}'):
            self._select_branches.select_option(branches)
            assertions.assert_eq(
                actual_value=self.get_selected_branches(),
                expected_value=branches,
                allure_title='Проверяем выбранное количество отводов',
                error_message=f'Несоответствие выбранного количества отводов'
            )

    def get_selected_connection(self) -> str:
        """
        Получение выбранного подключения
        :return: Текст выбранного значения
        """
        with allure.step(f'{self.NAME_PAGE} Получение выбранного подключения'):
            return self._select_connection.get_selected_text()

    def select_connection(self, connection: str) -> None:
        """
        Выбор подключения
        :param connection: Текст опции для выбора
        """
        with allure.step(f'{self.NAME_PAGE} Выбор подключения: {connection}'):
            self._select_connection.select_option(connection)
            assertions.assert_eq(
                actual_value=self.get_selected_connection(),
                expected_value=connection,
                allure_title='Проверяем выбранное подключение',
                error_message=f'Несоответствие выбранного подключения'
            )

    def get_selected_collector(self) -> str:
        """
        Получение выбранного коллектора
        :return: Текст выбранного значения
        """
        with allure.step(f'{self.NAME_PAGE} Получение выбранного коллектора'):
            return self._select_collector.get_selected_text()

    def select_collector(self, collector: str) -> None:
        """
        Выбор коллектора
        :param collector: Текст опции для выбора
        """
        with allure.step(f'{self.NAME_PAGE} Выбор коллектора: {collector}'):
            self._select_collector.select_option(collector)
            assertions.assert_eq(
                actual_value=self.get_selected_collector(),
                expected_value=collector,
                allure_title='Проверяем выбранный коллектор',
                error_message=f'Несоответствие выбранного коллектора'
            )

    def get_selected_reducer(self) -> str:
        """
        Получение выбранного редуктора
        :return: Текст выбранного значения
        """
        with allure.step(f'{self.NAME_PAGE} Получение выбранного редуктора'):
            return self._select_reducer.get_selected_text()

    def select_reducer(self, reducer: str) -> None:
        """
        Выбор редуктора
        :param reducer: Текст опции для выбора
        """
        with allure.step(f'{self.NAME_PAGE} Выбор редуктора: {reducer}'):
            self._select_reducer.select_option(reducer)
            assertions.assert_eq(
                actual_value=self.get_selected_reducer(),
                expected_value=reducer,
                allure_title='Проверяем выбранный редуктор',
                error_message=f'Несоответствие выбранного редуктора'
            )

    def get_selected_branch_dn(self) -> str:
        """
        Получение выбранного Ду арматуры на отводах
        :return: Текст выбранного значения
        """
        with allure.step(f'{self.NAME_PAGE} Получение выбранного Ду арматуры на отводах'):
            return self._select_branch_dn.get_selected_text()

    def select_branch_dn(self, dn: str) -> None:
        """
        Выбор Ду арматуры на отводах
        :param dn: Текст опции для выбора
        """
        with allure.step(f'{self.NAME_PAGE} Выбор Ду арматуры на отводах: {dn}'):
            self._select_branch_dn.select_option(dn)
            assertions.assert_eq(
                actual_value=self.get_selected_branch_dn(),
                expected_value=dn,
                allure_title='Проверяем выбранный Ду арматуры на отводах',
                error_message=f'Несоответствие выбранного Ду арматуры на отводах'
            )

    def get_selected_inlet_dn(self) -> str:
        """
        Получение выбранного Ду арматуры на вводе
        :return: Текст выбранного значения
        """
        with allure.step(f'{self.NAME_PAGE} Получение выбранного Ду арматуры на вводе'):
            return self._select_inlet_dn.get_selected_text()

    def select_inlet_dn(self, dn: str) -> None:
        """
        Выбор Ду арматуры на вводе
        :param dn: Текст опции для выбора
        """
        with allure.step(f'{self.NAME_PAGE} Выбор Ду арматуры на вводе: {dn}'):
            self._select_inlet_dn.select_option(dn)
            assertions.assert_eq(
                actual_value=self.get_selected_inlet_dn(),
                expected_value=dn,
                allure_title='Проверяем выбранный Ду арматуры на вводе',
                error_message=f'Несоответствие выбранного Ду арматуры на вводе'
            )

    def should_params_match(self, params: dict) -> None:
        """
        Проверка что все параметры соответствуют ожидаемым
        :param params: Словарь с ожидаемыми значениями параметров
        """
        with allure.step(f'{self.NAME_PAGE} Проверка соответствия всех параметров'):
            self._select_node_type.wait_presence_in_located_dom()
            assertions.assert_eq(self.get_selected_node_type(), params['node_type'],
                                 allure_title='Тип узла', error_message='Несоответствие типа узла')
            assertions.assert_eq(self.get_selected_branches(), params['branches'],
                                 allure_title='Количество отводов', error_message='Несоответствие количества отводов')
            assertions.assert_eq(self.get_selected_connection(), params['connection'],
                                 allure_title='Подключение', error_message='Несоответствие подключения')
            assertions.assert_eq(self.get_selected_collector(), params['collector'],
                                 allure_title='Коллектор', error_message='Несоответствие коллектора')
            assertions.assert_eq(self.get_selected_reducer(), params['reducer'],
                                 allure_title='Редуктор', error_message='Несоответствие редуктора')
            assertions.assert_eq(self.get_selected_branch_dn(), params['branch_dn'],
                                 allure_title='Ду арматуры на отводах',
                                 error_message='Несоответствие Ду арматуры на отводах')
            assertions.assert_eq(self.get_selected_inlet_dn(), params['inlet_dn'],
                                 allure_title='Ду арматуры на вводе',
                                 error_message='Несоответствие Ду арматуры на вводе')