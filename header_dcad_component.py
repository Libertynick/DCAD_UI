import allure
from selenium.webdriver.chrome.webdriver import WebDriver

from components.base_component import BaseComponent
from elements.button import Button


class HeaderDcadComponent(BaseComponent):
    """
    Шапка сайта DCAD
    Содержит кнопки навигации и элементы авторизации
    """
    NAME_PAGE = "|Шапка сайта DCAD|"

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

        # Buttons - навигация
        self._btn_configurator_tdu = Button(
            driver,
            "//a[text()='Конфигуратор TDU']","Конфигуратор TDU"
        )
        self._btn_login = Button(
            driver,
            "//a[@class='nav-link' and @id='loginLink']","Кнопка Войти"
        )
        self._text_user_email = Button(
            driver,
            "//a[@class='nav-link' and @title='Manage']","Email авторизированного пользователя"
        )

    def click_login_button(self) -> None:
        """Клик по кнопке Войти"""
        with allure.step('Клик по кнопке Войти в шапке DCAD'):
            self._btn_login.click()

    def click_btn_configurator_tdu(self) -> None:
        """Клик по кнопке Войти"""
        with allure.step('Клик по кнопке Войти в шапке DCAD'):
            self._btn_configurator_tdu.click()

    def is_user_logged_in(self) -> bool:
        """
        Проверка, что пользователь авторизован
        :return: True если пользователь авторизован, False если нет
        """
        with allure.step('Проверка авторизации пользователя в DCAD'):
            elements = self._text_user_email.find_elements_safely()
            is_logged = len(elements) > 0
            if is_logged:
                print(f'Пользователь авторизован')
            else:
                print(f'Пользователь НЕ авторизован')
            return is_logged
