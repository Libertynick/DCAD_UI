import allure
from selenium.webdriver.chrome.webdriver import WebDriver

from components.base_component import BaseComponent
from components.open_components.header_component.profile_menu_component import ProfileMenuComponent
from components.open_components.loader_component import LoaderComponent
from elements.button import Button
from open_pages.cart_page.cart_page import CartPage
from open_pages.selection_tools_modal.selection_tools_modal import OnlineSelectionModal


class NavBarRidan(BaseComponent):
    """
    Компонент nav bar Ridan.
    В данный компонент входят:
    • Логотип компании Ридан
    • Кнопка Каталог
    • Кнопка Побор онлайн
    • Поле ввода "поиск по сайту", кнопка Искать
    • Кнопка Уведомления
    • Кнопка Корзина
    • Кнопка меню профиля, отображается как имя пользователя
    """

    NAME_PAGE = 'Шапка сайта Ридан'

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

        # Компоненты
        self.loader_component = LoaderComponent(self.driver)
        self.cart_page = CartPage(self.driver)
        self.profile_menu_component = ProfileMenuComponent(self.driver)
        self.online_selection_modal = OnlineSelectionModal(driver)

        # Кнопки
        self.btn_to_come_in = Button(driver, "//a[@data-hash-click='auth']/parent::li", "Войти")
        self.btn_profile = Button(driver, "//a[@class='profile__dropdown__button']/span", "Профиль")
        self.btn_cart = Button(driver, "//span[text()='Корзина']", "Корзина")
        self.btn_online_selection = Button(driver, "//button[@data-instruments-btn-open]", "Подбор онлайн")

    def click_btn_basket(self):
        """Клик по кнопке Корзина"""
        with allure.step('Клик по кнопке Корзина'):
            self.btn_cart.click()
            self.cart_page.should_header_cart()
            self.cart_page.wait_no_visible_header_update_cart()
            self.loader_component.waiting_for_loader_no_text_processing_on_page()

    def opened_profile_menu(self):
        """Раскрытие меню профиля"""
        with allure.step('Раскрытие меню профиля'):
            self.btn_profile.click()
            self.profile_menu_component.ul_profile_menu.wait_visible_on_page()

    def click_btn_online_selection(self):
        """Клик по кнопке Подбор онлайн"""
        with allure.step('Клик по кнопке Подбор онлайн'):
            self.btn_online_selection.click()
            self.online_selection_modal.section_online_selection_opened.wait_visible_on_page()
