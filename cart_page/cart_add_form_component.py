import allure
from selenium.webdriver.chrome.webdriver import WebDriver

from components.base_component import BaseComponent
from components.open_components.loader_component import LoaderComponent

from elements.button import Button
from elements.input import Input
from elements.text import Text
from elements.ul_list import UlList


class CartAddFormComponent(BaseComponent):
    """
    Компонент Форма добавления товара в корзину (поле добавления, кнопка Добавить, выбор условий покупки)
    Скриншот компонента: docs/images_component_open/cart_components/cart_add_form_component.png
    """

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

        self._loader_component = LoaderComponent(driver)

        # button
        self._btn_activate_ul_client_number = Button(
            driver,
            "//div[@data-id='cart-purchase-single-select-title']/div[@class='single-select__value-title-icon']",
            'Активации выпадающего списка Условия покупки'
        )
        self._btn_add = Button(driver, "//button[@data-id='cart-add-position-btn']", "Добавить")

        # Выпадающие списки
        self._ul_client_number = UlList(
            driver,
            "//ul[@data-id='cart-purchase-single-select-box']", "Клиентские номера")

        # Текстовые элементы
        self._client_number_in_ul_by_number = Text(
            driver,
            "//ul[@data-id='cart-purchase-single-select-box']//span[text()='{num_client}']",
            "Клиентский номер в выпадающем списке Условия покупки по номеру")
        self._selected_terms_of_purchase = Text(
            driver,
            "//div[@data-id='cart-purchase-single-select-title']//span[text()]",
            "Выбранные условия покупки")

        # input
        self._product_input = Input(driver, "//input[@name='search']", "Ввод артикулов")

    def click_add_button(self) -> None:
        """Клик по кнопке Добавить"""
        with allure.step('Клик по кнопке Добавить в корзине'):
            self._btn_add.click()
            self._loader_component.waiting_for_loader_text_processing_on_page(timeout=60)

    def choice_of_client_number(self, number_client='RT25-7705238125-HE') -> None:
        """Выбор клиентского номера"""
        with allure.step(f'Выбор клиентского номера {number_client}'):
            self._btn_activate_ul_client_number.click(timeout=3)
            self._ul_client_number.wait_visible_on_page()
            self._client_number_in_ul_by_number.click(num_client=number_client)

            self._loader_component.waiting_for_loader_no_text_processing_on_page()
            self._loader_component.waiting_for_loader_text_processing_on_page()

            self._selected_terms_of_purchase.should_text_in_element(expected_text=number_client)

    def should_selected_terms_of_purchase(self, expected_terms_of_purchase: str) -> None:
        """
        Должны быть выбраны определенные условия покупки
        :param expected_terms_of_purchase: Ожидаемые выбранные условия покупки
        """
        self._loader_component.waiting_for_loader_no_text_processing_on_page()
        try:
            self._selected_terms_of_purchase.should_text_in_element(expected_text=expected_terms_of_purchase)
        except AssertionError:
            self._loader_component.waiting_for_loader_no_text_processing_on_page()
            self._selected_terms_of_purchase.should_text_in_element(expected_text=expected_terms_of_purchase)

    def type_product_in_input(self, article: str or list):
        """
        Ввод артикула в поле внесения
        :param article: Артикулы для ввода
        """
        with allure.step(f'Ввод артикула {article} в поле ввода корзины'):
            if type(article) is str:
                article = ' '.join(article.split())

            elif type(article) is list:
                article = ' '.join(' '.join(article).split())

            self._product_input.clear_input()
            self._product_input.filling_input(article)
            self._product_input.should_value_in_input_field(article)
