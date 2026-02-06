import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from base_page.base_page import BasePage
from components.open_components.loader_component import LoaderComponent
from components.open_components.modal_equipment_cost_calculation import ModalEquipmentCostCalculation

from elements.text import Text
from open_pages.cart_page.cart_add_form_component import CartAddFormComponent

from open_pages.cart_page.cart_summary_component import CartSummaryComponent
from open_pages.cart_page.list_article_component import ListArticleComponent
from open_pages.cart_page.toolbar_component import ToolbarComponent


@allure.feature('Страница Корзина')
class CartPage(BasePage):
    """Страница Корзина"""

    def __init__(self, driver: WebDriver, url: str = 'https://ruecom-open-tst1.ridancorp.net/sales/cart'):
        super().__init__(driver, url)

        # components
        self.loader_component = LoaderComponent(driver)
        self.toolbar_component_cart = ToolbarComponent(driver)
        self.cart_add_form_component = CartAddFormComponent(driver)
        self.list_article_in_cart_component = ListArticleComponent(driver)
        self.cart_summary_component = CartSummaryComponent(driver)
        self.modal_equipment_cost_calculation = ModalEquipmentCostCalculation(driver)

        # Текстовые элементы
        self._header_cart = Text(driver, "//h1[text()='Корзина']", "Заголовок Корзина")
        self._header_update_cart = Text(driver, "//h2[contains(text(), 'Обновление корзины...')]",
                                        "Заголовок Обновление корзины")
        self._header_cart_is_empty = Text(driver, "//h2[text()=' Корзина пуста ']", "Заголовок Корзина пуста")

    def should_header_cart(self) -> None:
        """Должен отображаться заголовок Корзина"""
        with allure.step(f'Проверка, что отображается заголовок {self._header_cart.name}'):
            self._header_cart.wait_visible_on_page()

    def wait_no_visible_header_update_cart(self) -> None:
        """Должен быть заголовок Обновление корзины"""
        with allure.step(f'Проверка отображения заголовка {self._header_update_cart.name}'):
            header_update_cart = len(self._header_update_cart.find_elements_safely())
            if header_update_cart:
                self._header_update_cart.wait_no_visible_on_page(timeout=60)
