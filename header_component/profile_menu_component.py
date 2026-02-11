import allure
from selenium.webdriver.chrome.webdriver import WebDriver

from components.base_component import BaseComponent
from components.open_components.loader_component import LoaderComponent
from elements.button import Button
from elements.text import Text
from elements.ul_list import UlList
from open_pages.ridan_online_pages.list_order_ridan_online_page import ListOrderRidanOnlinePage


class ProfileMenuComponent(BaseComponent):
    """
    Компонент меню профиля в виде выпадающего списка
    """

    NAME_PAGE = '|Меню Профиль пользователя в Опен|'

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

        # Компоненты
        self._loader = LoaderComponent(driver)
        self.list_order_ridan_online = ListOrderRidanOnlinePage(driver)

        # Текстовые элементы
        self.name_company = Text(driver, "//span[@class='company-name']", "Название компании")
        self.name_profile = Text(driver, "//span[@class='profile-name']", "Наименование профиля")

        # Выпадающие списки ul
        self.ul_profile_menu = UlList(driver, "//ul[@class='profile__dropdown show']", "Профиль")
        self._ul_calculations = UlList(driver, "//div[@id='vertical-cabinet-calculations']//ul", "Расчеты")

        # Кнопки
        self.btn_objects = Button(driver, "//a[@data-bs-target='#vertical-cabinet-objects']", "Объекты")
        self.btn_fastening_request = Button(
            driver,
            "//a[@href='/cabinet/objects/applications-for-attachment']", "Заявки на крепление")
        self.btn_drop_order_menu = Button(driver,
                                          "//a[@data-bs-target='#vertical-cabinet-orders' and @id='dropdownMenuLink']",
                                          "Заказы. Открыть/Закрыть выпадающее меню")
        self.btn_order_ridan_online = Button(driver,
                                             "//div[@id='vertical-cabinet-orders' and @data-bs-parent='#accordion-vertical-cabinet-orders']//a[@href='/cabinet/orders/ridan-online']",
                                             "Заказы Ридан онлайн")
        self._btn_design_condition = Button(driver, "//a[@href='/cabinet/project-conditions']", "Проектные условия")
        self.btn_orders = Button(driver, "//ul[@class='profile__dropdown show']//a[@href='/cabinet/orders']", "Заказы")
        self._btn_calculation = Button(driver, "//a[@data-bs-target='#vertical-cabinet-calculations']", "Расчеты")
        self._btn_calculation_and_ol_pto = Button(driver, "//a[@href='/cabinet/calculations/pto']", "Расчеты и ОЛ ПТО")

    def opened_ul_menu_order(self):
        """Раскрытие выпадающего меню Заказы"""
        with allure.step(f'{self.NAME_PAGE}. Раскрытие выпадающего меню Заказы'):
            self.btn_drop_order_menu.click()
            self.btn_order_ridan_online.wait_visible_on_page()

    def click_btn_order_ridan_online(self):
        """Клик по кнопке Заказы Ридан онлайн"""
        with allure.step(f'{self.NAME_PAGE}. Клик по кнопке Заказы Ридан онлайн'):
            self.opened_ul_menu_order()
            self.btn_order_ridan_online.click()
            self._loader.waiting_for_loader_no_text_processing_on_page()
            self.list_order_ridan_online.header.wait_visible_on_page()

    def save_name_distributor(self) -> str:
        """Сохранение наименования компании дистрибьютора"""
        with allure.step(f'{self.NAME_PAGE}. Сохранение наименования компании дистрибьютора'):
            self.name_company.wait_presence_in_located_dom()
            return self.name_company.get_text_element()

    def save_name_client(self) -> str:
        """Сохранение имени клиента"""
        with allure.step(f'{self.NAME_PAGE}. Сохранение имени клиента'):
            self.name_profile.wait_presence_in_located_dom()
            return self.name_profile.get_text_element()

    def click_item_order(self):
        """Переход в Заказы"""
        with allure.step(f'{self.NAME_PAGE}. Переход в Заказы'):
            self.btn_orders.click()
            self._loader.waiting_for_loader_no_text_processing_on_page()

    def click_btn_calculations(self) -> None:
        """Клик по кнопке Расчеты"""
        with allure.step(f'Клик по кнопке {self._btn_calculation.name}'):
            self._btn_calculation.click()
            self._ul_calculations.wait_visible_on_page()

    def click_btn_calculations_and_ol_pto(self) -> None:
        """Клик по кнопке Расчеты и ОЛ ПТО"""
        with allure.step(f'Клик по кнопке {self._btn_calculation_and_ol_pto.name}'):
            self._btn_calculation_and_ol_pto.click()
            self._loader.waiting_for_loader_no_text_processing_on_page()

    def go_to_design_condition(self) -> None:
        """Переход в Проектные условия"""
        with allure.step(f'{self.NAME_PAGE} Переход в Проектные условия'):
            self._btn_design_condition.click()
            self._loader.waiting_for_loader_no_text_processing_on_page()
