import allure
from selenium.webdriver.chrome.webdriver import WebDriver

from components.base_component import BaseComponent
from elements.options import Options
from elements.text import Text
from tools.validators import assertions


class TduConfigFilterComponent(BaseComponent):
    """
    Компонент формы фильтров на странице Конфигуратор TDU (Config)
    Содержит фильтры: Тип узла, Отводов, Стояк, Клапан на подаче, Ду ввода, Клап. на отводах
    и дропдаун выбора готовой конфигурации узла
    """

    NAME_PAGE = '|Страница конфигуратор ТДУ (config)|'

    RISER_TO_LETTER = {
        'Слева': 'L',
        'Справа': 'R',
    }

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

        # Options
        self._option_node_type = Options(
            driver,
            "//select[@id='TduFamilyId']",
            "Тип узла"
        )
        self._option_branches = Options(
            driver,
            "//select[@id='outputsCount']",
            "Отводов"
        )
        self._option_riser = Options(
            driver,
            "//select[@id='isLeft']",
            "Стояк"
        )
        self._option_supply_valve = Options(
            driver,
            "//select[@data-bind='value: hasPartner']",
            "Клапан на подаче"
        )
        self._option_inlet_diameter = Options(
            driver,
            "//select[@id='inputDn']",
            "Ду ввода"
        )
        self._option_branch_valves = Options(
            driver,
            "//select[@id='outputValve']",
            "Клап. на отводах"
        )
        self._option_ready_config = Options(
            driver,
            "//select[@id='CalculationId']",
            "Готовая конфигурация узла"
        )

        # Text
        self._ready_config_first_option = Text(
            driver,
            "//select[@id='CalculationId']/option[position()>1]",
            "Первая опция готовой конфигурации узла"
        )

    def select_node_type(self, value: str) -> None:
        """Выбор типа узла"""
        with allure.step(f'{self.NAME_PAGE} Выбор типа узла: {value}'):
            self._option_node_type.select_option(value)
            selected = self._option_node_type.get_selected_text()
            assertions.assert_eq(
                actual_value=selected,
                expected_value=value,
                allure_title='Проверяем выбранный тип узла',
                error_message=f'Несоответствие выбранного типа узла. На странице - {selected}; ожидаемое - {value}'
            )

    def select_branches(self, value: str) -> None:
        """Выбор количества отводов"""
        with allure.step(f'{self.NAME_PAGE} Выбор количества отводов: {value}'):
            self._option_branches.select_option(value)
            selected = self._option_branches.get_selected_text()
            assertions.assert_eq(
                actual_value=selected,
                expected_value=value,
                allure_title='Проверяем выбранное кол-во отводов',
                error_message=f'Несоответствие выбранного кол-ва отводов. На странице - {selected}; ожидаемое - {value}'
            )

    def select_riser(self, value: str) -> None:
        """Выбор стояка"""
        with allure.step(f'{self.NAME_PAGE} Выбор стояка: {value}'):
            self._option_riser.select_option(value)
            selected = self._option_riser.get_selected_text()
            assertions.assert_eq(
                actual_value=selected,
                expected_value=value,
                allure_title='Проверяем выбранный стояк',
                error_message=f'Несоответствие выбранного стояка. На странице - {selected}; ожидаемое - {value}'
            )

    def select_supply_valve(self, value: str) -> None:
        """Выбор клапана на подаче"""
        with allure.step(f'{self.NAME_PAGE} Выбор клапана на подаче: {value}'):
            self._option_supply_valve.select_option(value)
            selected = self._option_supply_valve.get_selected_text()
            assertions.assert_eq(
                actual_value=selected,
                expected_value=value,
                allure_title='Проверяем выбранный клапан на подаче',
                error_message=f'Несоответствие выбранного клапана на подаче. На странице - {selected}; ожидаемое - {value}'
            )

    def select_inlet_diameter(self, value: str) -> None:
        """Выбор диаметра ввода"""
        with allure.step(f'{self.NAME_PAGE} Выбор Ду ввода: {value}'):
            self._option_inlet_diameter.select_option(value)
            selected = self._option_inlet_diameter.get_selected_text()
            assertions.assert_eq(
                actual_value=selected,
                expected_value=value,
                allure_title='Проверяем выбранный Ду ввода',
                error_message=f'Несоответствие выбранного Ду ввода. На странице - {selected}; ожидаемое - {value}'
            )

    def select_branch_valves(self, value: str) -> None:
        """Выбор клапанов на отводах"""
        with allure.step(f'{self.NAME_PAGE} Выбор клапанов на отводах: {value}'):
            self._option_branch_valves.select_option(value)
            selected = self._option_branch_valves.get_selected_text()
            assertions.assert_eq(
                actual_value=selected,
                expected_value=value,
                allure_title='Проверяем выбранные клапаны на отводах',
                error_message=f'Несоответствие выбранных клапанов на отводах. На странице - {selected}; ожидаемое - {value}'
            )

    def select_ready_config(self, value: str) -> None:
        """Выбор готовой конфигурации узла"""
        with allure.step(f'{self.NAME_PAGE} Выбор готовой конфигурации узла: {value}'):
            self._option_ready_config.wait_visible_on_page(timeout=10.0)
            self._option_ready_config.select_option(value)
            selected = self._option_ready_config.get_selected_text()
            assertions.assert_eq(
                actual_value=selected,
                expected_value=value,
                allure_title='Проверяем выбранную конфигурацию узла',
                error_message=f'Несоответствие выбранной конфигурации. На странице - {selected}; ожидаемое - {value}'
            )

    def get_selected_node_type(self) -> str:
        """Получение выбранного типа узла"""
        with allure.step(f'{self.NAME_PAGE} Получение выбранного типа узла'):
            return self._option_node_type.get_selected_text()

    def get_selected_branches(self) -> str:
        """Получение выбранного количества отводов"""
        with allure.step(f'{self.NAME_PAGE} Получение выбранного количества отводов'):
            return self._option_branches.get_selected_text()

    def get_selected_riser(self) -> str:
        """Получение выбранного стояка"""
        with allure.step(f'{self.NAME_PAGE} Получение выбранного стояка'):
            return self._option_riser.get_selected_text()

    def get_selected_inlet_diameter(self) -> str:
        """Получение выбранного Ду ввода"""
        with allure.step(f'{self.NAME_PAGE} Получение выбранного Ду ввода'):
            return self._option_inlet_diameter.get_selected_text()

    def get_selected_branch_valves(self) -> str:
        """Получение выбранных клапанов на отводах"""
        with allure.step(f'{self.NAME_PAGE} Получение выбранных клапанов на отводах'):
            return self._option_branch_valves.get_selected_text()

    def get_selected_ready_config(self) -> str:
        """Получение выбранной конфигурации узла"""
        with allure.step(f'{self.NAME_PAGE} Получение выбранной конфигурации узла'):
            return self._option_ready_config.get_selected_text()

    def get_first_available_config(self) -> str:
        """Получение первой доступной конфигурации из дропдауна (не плейсхолдер)"""
        with allure.step(f'{self.NAME_PAGE} Получение первой доступной конфигурации узла'):
            self._ready_config_first_option.wait_presence_in_located_dom(timeout=15.0)
            return self._ready_config_first_option.get_text_element()

    def should_ready_config_matches_filters(self, expected_type_contains: str) -> None:
        with allure.step(f'{self.NAME_PAGE} Проверка соответствия конфигурации текущим фильтрам'):
            selected = self.get_selected_ready_config()
            branches = self.get_selected_branches()
            riser = self.get_selected_riser()
            inlet_diameter = self.get_selected_inlet_diameter()
            branch_valve = self.get_selected_branch_valves()

            riser_letter = self.RISER_TO_LETTER[riser]
            valve_prefix = branch_valve.split('-')[0]

            assertions.assert_contains(
                actual_value=selected,
                expected_contains=expected_type_contains,
                allure_title='Проверяем тип узла в названии конфигурации',
                error_message=f'Тип узла "{expected_type_contains}" не найден в конфигурации "{selected}"'
            )
            assertions.assert_contains(
                actual_value=selected,
                expected_contains=f'{branches}{riser_letter}',
                allure_title='Проверяем кол-во отводов и стояк в названии конфигурации',
                error_message=f'Отводы+стояк "{branches}{riser_letter}" не найдены в конфигурации "{selected}"'
            )
            assertions.assert_contains(
                actual_value=selected,
                expected_contains=inlet_diameter,
                allure_title='Проверяем Ду ввода в названии конфигурации',
                error_message=f'Ду ввода "{inlet_diameter}" не найдено в конфигурации "{selected}"'
            )
            assertions.assert_contains(
                actual_value=selected,
                expected_contains=valve_prefix,
                allure_title='Проверяем клапан на отводах в названии конфигурации',
                error_message=f'Клапан "{valve_prefix}" не найден в конфигурации "{selected}"'
            )