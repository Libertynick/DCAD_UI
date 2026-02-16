import allure
from selenium.webdriver.chrome.webdriver import WebDriver

from components.base_component import BaseComponent
from elements.button import Button
from elements.input import Input
from elements.text import Text


class AuthorizationDcadModal(BaseComponent):
    """
    Модальное окно / Форма авторизации в DCAD
    """

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

        # Input поля
        self._input_email = Input(
            driver,
            "//input[@id='Email']",
            "Поле Email"
        )
        self._input_password = Input(
            driver,
            "//input[@id='Password']",
            "Поле Пароль"
        )

        # Button
        self._btn_submit = Button(
            driver,
            "//input[@type='submit']",
            "Кнопка Войти"
        )

        # Text - напоминание пароля (для проверки отображения)
        self._password_missing = Text(
            driver,
            "//a[text()='Забыли пароль?']",
            "Напоминание пароля"
        )

    def should_header_visible(self) -> None:
        """Проверка отображения заголовка формы авторизации"""
        with allure.step('Проверка отображения формы авторизации'):
            self._password_missing.wait_visible_on_page(timeout=5)

    def filling_email(self, email: str) -> None:
        """
        Заполнение поля Email
        :param email: Email для входа
        """
        with allure.step(f'Заполнение поля Email: {email}'):
            self._input_email.filling_input(email)

    def filling_password(self, password: str) -> None:
        """
        Заполнение поля Пароль
        :param password: Пароль для входа
        """
        with allure.step('Заполнение поля Пароль'):
            self._input_password.filling_input(password)

    def click_btn_submit(self) -> None:
        """Клик по кнопке Войти"""
        with allure.step('Клик по кнопке Войти'):
            self._btn_submit.click()