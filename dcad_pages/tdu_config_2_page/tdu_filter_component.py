import allure
from selenium.webdriver.chrome.webdriver import WebDriver

from base_page.base_page import BasePage
from components.base_component import BaseComponent
from components.open_components.loader_component import LoaderComponent

from elements.button import Button
from elements.options import Options
from elements.text import Text
from elements.ul_list import UlList


class TduFilterComponent(BaseComponent):
    """
    Компонент Форма фильтров на странице списка TDU
    Содержит 6 фильтров: Тип узла, Отводов, Стояк, Ду ввода, Клапан-партнёр, Клапаны на отводах
    Скриншот компонента: docs/images_component_dcad/tdu_list_page/tdu_filter_component.png
    """

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

        self._base_page = BasePage(driver)

        # ===== DROPDOWN FILTERS =====

        self._dropdown_node_type = Options(
            driver,
            "//select[@id='TduFamilySizeId']",
            "Тип узла"
        )

        self._dropdown_branches = Options(
            driver,
            "//select[@id='outputsCount']",
            "Отводов"
        )

        self._dropdown_riser = Options(
            driver,
            "//select[@id='isLeft']",
            "Стояк"
        )

        self._dropdown_inlet_diameter = Options(
            driver,
            "//select[@id='inputDn']",
            "Ду ввода"
        )

        self._dropdown_partner_valve = Options(
            driver,
            "//select[@data-bind='value: hasPartner']",
            "Клапан-партнёр"
        )

        self._dropdown_branch_valves = Options(
            driver,
            "//select[@id='outputValve']",
            "Клапаны на отводах"
        )


    def select_node_type(self, node_type: str) -> None:
        """Выбор типа узла"""
        with allure.step(f'Выбор типа узла: {node_type}'):
            self._dropdown_node_type.select_option(node_type)

    def select_branches(self, branches: str) -> None:
        """Выбор количества отводов"""
        with allure.step(f'Выбор количества отводов: {branches}'):
            self._dropdown_branches.select_option(branches)

    def select_riser(self, riser: str) -> None:
        """Выбор стояка"""
        with allure.step(f'Выбор стояка: {riser}'):
            self._dropdown_riser.select_option(riser)

    def select_inlet_diameter(self, diameter: str) -> None:
        """Выбор диаметра ввода"""
        with allure.step(f'Выбор Ду ввода: {diameter}'):
            self._dropdown_inlet_diameter.select_option(diameter)

    def select_partner_valve(self, valve: str) -> None:
        """Выбор клапана-партнёра"""
        with allure.step(f'Выбор клапана-партнёра: {valve}'):
            self._dropdown_partner_valve.select_option(valve)

    def select_branch_valves(self, valves: str) -> None:
        """Выбор клапанов на отводах"""
        with allure.step(f'Выбор клапанов на отводах: {valves}'):
            self._dropdown_branch_valves.select_option(valves)

    def set_filters(self, node_type: str = None, branches: str = None, riser: str = None,
                    inlet_diameter: str = None, partner_valve: str = None,
                    branch_valves: str = None) -> None:
        """Установка нескольких фильтров одновременно"""
        with allure.step('Установка фильтров для поиска TDU'):
            if node_type:
                self.select_node_type(node_type)
            if branches:
                self.select_branches(branches)
            if riser:
                self.select_riser(riser)
            if inlet_diameter:
                self.select_inlet_diameter(inlet_diameter)
            if partner_valve:
                self.select_partner_valve(partner_valve)
            if branch_valves:
                self.select_branch_valves(branch_valves)

    def get_selected_node_type(self) -> str:
        """Получение выбранного типа узла"""
        with allure.step('Получение выбранного типа узла'):
            return self._dropdown_node_type.get_selected_text()

    def get_selected_branches(self) -> str:
        """Получение выбранного количества отводов"""
        with allure.step('Получение выбранного количества отводов'):
            return self._dropdown_branches.get_selected_text()