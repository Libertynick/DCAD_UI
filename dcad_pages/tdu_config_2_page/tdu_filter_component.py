import allure
from selenium.webdriver.chrome.webdriver import WebDriver

from base_page.base_page import BasePage
from components.base_component import BaseComponent

from elements.options import Options
from tools.validators import assertions


class TduFilterComponent(BaseComponent):
    """
    Компонент Форма фильтров на странице списка TDU
    Содержит 6 фильтров: Тип узла, Отводов, Стояк, Ду ввода, Клапан-партнёр, Клапаны на отводах
    Скриншот компонента: docs/images_component_dcad/tdu_list_page/tdu_filter_component.png
    """

    NAME_PAGE = '|Страница конфигуратор ТДУ (config2)|'

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

        self._base_page = BasePage(driver)

        # Option
        self._option_dropdown_node_type = Options(
            driver,
            "//select[@id='TduFamilySizeId']","Тип узла"
        )

        self._option_dropdown_branches = Options(
            driver,
            "//select[@id='outputsCount']","Отводов"
        )

        self._option_dropdown_riser = Options(
            driver,
            "//select[@id='isLeft']","Стояк"
        )

        self._option_dropdown_inlet_diameter = Options(
            driver,
            "//select[@id='inputDn']","Ду ввода"
        )

        self._option_dropdown_partner_valve = Options(
            driver,
            "//select[@data-bind='value: hasPartner']","Клапан-партнёр"
        )

        self._option_dropdown_branch_valves = Options(
            driver,
            "//select[@id='outputValve']","Клапаны на отводах"
        )

    def select_node_type(self, node_type: str) -> None:
        """Выбор типа узла"""
        with allure.step(f'{self.NAME_PAGE} Выбор типа узла: {node_type}'):
            self._option_dropdown_node_type.select_option(node_type)
            selected_value = self.get_selected_node_type()

            assertions.assert_eq(
                actual_value=selected_value,
                expected_value=node_type,
                allure_title='Проверяем выбранный тип узла',
                error_message=f'Несоответствие выбранного типа узла'
            )

    def select_branches(self, branches: str) -> None:
        """Выбор количества отводов"""
        with allure.step(f'{self.NAME_PAGE}Выбор количества отводов: {branches}'):
            self._option_dropdown_branches.select_option(branches)
            selected_value = self.get_selected_branches()

            assertions.assert_eq(
                actual_value=selected_value,
                expected_value=branches,
                allure_title='Проверяем выбранное кол-во отводов',
                error_message=f'Несоответствие выбранного кол-ва отводов'
            )

    def select_riser(self, riser: str) -> None:
        """Выбор стояка"""
        with allure.step(f'{self.NAME_PAGE} Выбор стояка: {riser}'):
            self._option_dropdown_riser.select_option(riser)
            selected_value = self.get_selected_riser()

            assertions.assert_eq(
                actual_value=selected_value,
                expected_value=riser,
                allure_title='Проверяем выбранную ориентацию стояка',
                error_message=f'Несоответствие выбранного кол-ва отводов'
            )

    def select_inlet_diameter(self, diameter: str) -> None:
        """Выбор диаметра ввода"""
        with allure.step(f'{self.NAME_PAGE} Выбор Ду ввода: {diameter}'):
            self._option_dropdown_inlet_diameter.select_option(diameter)
            selected_value = self.get_selected_inlet_diameter()

            assertions.assert_eq(
                actual_value=selected_value,
                expected_value=diameter,
                allure_title='Проверяем выбранный диаметр ввода',
                error_message=f'Несоответствие выбранного диаметра ввода'
            )

    def select_partner_valve(self, valve: str) -> None:
        """Выбор клапана-партнёра"""
        with allure.step(f'{self.NAME_PAGE} Выбор клапана-партнёра: {valve}'):
            self._option_dropdown_partner_valve.select_option(valve)
            selected_value = self.get_selected_partner_valve()

            assertions.assert_eq(
                actual_value=selected_value,
                expected_value=valve,
                allure_title='Проверяем наличие выбранного клапана-партнера',
                error_message=f'Несоответствие наличия выбранного клапана партнера'
            )

    def select_branch_valves(self, valves: str) -> None:
        """Выбор клапанов на отводах"""
        with allure.step(f'{self.NAME_PAGE} Выбор клапанов на отводах: {valves}'):
            self._option_dropdown_branch_valves.select_option(valves)
            selected_value = self.get_selected_branch_valves()

            assertions.assert_eq(
                actual_value=selected_value,
                expected_value=valves,
                allure_title='Проверяем выбранные клапаны на отводах',
                error_message=f'Несоответствие выбранных клапанов на отводах'
            )

    def get_selected_node_type(self) -> str:
        """Получение выбранного типа узла"""
        with allure.step(f'{self.NAME_PAGE} Получение выбранного типа узла'):
            return self._option_dropdown_node_type.get_selected_text()

    def get_selected_branches(self) -> str:
        """Получение выбранного количества отводов"""
        with allure.step(f'{self.NAME_PAGE} Получение выбранного количества отводов'):
            return self._option_dropdown_branches.get_selected_text()

    def get_selected_riser(self) -> str:
        """Получение выбранной конфигурации стояка"""
        with allure.step(f'{self.NAME_PAGE} Получение выбранной конфигурации стояка'):
            return self._option_dropdown_riser.get_selected_text()

    def get_selected_inlet_diameter(self) -> str:
        """Получение выбранного диаметра узла"""
        with allure.step(f'{self.NAME_PAGE} Получение выбранного диаметра узла'):
            return self._option_dropdown_inlet_diameter.get_selected_text()

    def get_selected_partner_valve(self) -> str:
        """Получение выбранного клапана партнера"""
        with allure.step(f'{self.NAME_PAGE} Получение выбранного клапана партнера'):
            return self._option_dropdown_partner_valve.get_selected_text()

    def get_selected_branch_valves(self) -> str:
        """Получение выбранного клапана на отводах"""
        with allure.step(f'{self.NAME_PAGE} Получение выбранного клапана на отводах'):
            return self._option_dropdown_branch_valves.get_selected_text()
