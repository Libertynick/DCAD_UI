import allure
from selenium.webdriver.chrome.webdriver import WebDriver

from base_page.base_page import BasePage
import time

from base_page.base_page_locators import BaseOpenLocators
from components.open_components.loader_component import LoaderComponent
from open_pages.header.header_locators import HeaderLocators
from open_pages.main_page.main_page_locators import AuthorizationModalLocators, MainPageLocators
from open_pages.registration_page.registration_page_locators import RegistrationPageLocators


@allure.feature('Главная страница')
class MainPage(BasePage):
    """Главная страница"""

    def __init__(self, driver: WebDriver, url: str = ''):
        super().__init__(driver, url)

        # Компоненты
        self.loader_component = LoaderComponent(driver)


@allure.feature('Модалка Авторизация')
class AuthorizationModal(BasePage):
    """Модалка Авторизация"""

    def click_btn_registration(self):
        """Клик по кнопке Регистрация"""
        with allure.step('Клик по кнопке Регистрация'):
            self.expecting_clickability(AuthorizationModalLocators.LOCATOR_BTN_REGISTRATION)
            btn_registration = self.find_element(AuthorizationModalLocators.LOCATOR_BTN_REGISTRATION)
            btn_registration.click()
            time.sleep(2)
            self.loader_open.waiting_for_loader_no_text_processing_on_page()
            self.waiting_element_is_visibility_on_the_page(RegistrationPageLocators.LOCATOR_HEADER_REGISTRATION)