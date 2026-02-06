import allure
from selenium.webdriver.chrome.webdriver import WebDriver

from base_page.base_page import BasePage
from base_page.base_page_locators import BaseOpenLocators
from open_pages.cart_page.cart_shared_page.cart_shared_page_locators import CartSharedPageLocators


@allure.feature('Страница С вами поделились корзиной')
class CartSharedPage(BasePage):
    """Страница С вами поделились корзиной"""

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def click_btn_clean_and_add_in_modal_shared_cart_with_you(self):
        """Клик по кнопке Очистить и добавить в модалке
        'С вами поделились корзиной, но в вашей корзине уже есть товары '"""
        with allure.step('Клик по кнопке Очистить и добавить в модалку в С вами поделились Корзиной'):
            btn_clean_and_add = self.find_element(
                CartSharedPageLocators.LOCATOR_BTN_CLEAN_AND_ADD_IN_MODAL_SHARED_CART_WITH_YOU)
            btn_clean_and_add.click()
            self.loader_open.waiting_for_loader_no_text_processing_on_page()

    def save_list_article_on_page(self) -> list:
        """Сохранение списка артикулов на странице без повторов"""
        with allure.step('Сохранение списка артиклов на старнице без повторов'):
            self.waiting_element_is_visibility_located_dom(CartSharedPageLocators.LOCATOR_ARTICLE)
            list_article = self.find_elements(CartSharedPageLocators.LOCATOR_ARTICLE)
            list_article = [article.text for article in list_article]
            return list(set(list_article))

    def click_btn_add_sales_page_shared_card(self):
        """Кнопка Добавить в корзину на странице С вами поделились Корзиной"""
        with allure.step('Кнопка Добавить в корзину на странице С вами поделились Корзиной'):
            self.waiting_element_is_visibility_on_the_page(CartSharedPageLocators.LOCATOR_BTN_ADD_SALES)
            # Определяем количество в корзине по отображению количества на иконке Корзина
            with allure.step('Определяем количество в корзине по отображению количества на иконке Корзина'):
                quantity_in_basket = self.driver.find_elements(
                    *CartSharedPageLocators.LOCATOR_QUANTITY_IN_CART_ON_CART_ICON)

                click_btn_add_sales_page_shared_card = self.find_element(CartSharedPageLocators.LOCATOR_BTN_ADD_SALES)
                self.driver.execute_script("arguments[0].click()", click_btn_add_sales_page_shared_card)
                self.waiting_for_loader_processing_on_page(BaseOpenLocators.LOCATOR_SPINNER_NO_TEXT)

                print(len(quantity_in_basket))
                if len(quantity_in_basket) == 0:
                    self.waiting_element_is_visibility_on_the_page(
                        CartSharedPageLocators.LOCATOR_HEADER_MODAL_SHARED_CART_WITH_YOU)
                    self.click_btn_clean_and_add_in_modal_shared_cart_with_you()
