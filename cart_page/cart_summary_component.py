import allure
from selenium.webdriver.chrome.webdriver import WebDriver

from components.base_component import BaseComponent
from components.open_components.loader_component import LoaderComponent
from elements.button import Button
from elements.text import Text
from open_pages.cart_page.list_article_component import ListArticleComponent
from tools.validators import assertions


class CartSummaryComponent(BaseComponent):
    """
    Компонент Итоговая стоимость корзины. Находится под списком артикулов.
    Содержит в себе различные информационные сообщения, итоговую стоимость и кнопку Продолжить
    Скриншот компонента: docs/images_component_open/cart_components/cart_summary_component.png
    """

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

        self._loader_component = LoaderComponent(driver)
        self._list_material_component = ListArticleComponent(driver)

        # button
        self._btn_continue = Button(driver, "//a[@data-id='cart-continue-btn']", "Продолжить")

        # Text
        self._total_price = Text(driver, "//div[@class='fs-4']//span[text()]", "Итого с НДС")

    def click_continue_button(self) -> None:
        """Клик по кнопке Продолжить"""
        with allure.step('Клик по кнопке Продолжить в корзине'):
            self._btn_continue.scroll_to_elem_action_chains()
            self._btn_continue.click()
            self._loader_component.waiting_for_loader_no_text_processing_on_page()

    def save_total_price(self) -> float:
        """Сохранение итоговой стоимости"""
        with allure.step('Сохранение итоговой стоимости'):
            total_price = self._total_price.get_float_value_from_line()
            return total_price

    def check_total_with_nds(self, expected_total_price: float) -> None:
        """
        Проверка итоговой стоимости с НДС
        :param expected_total_price: Ожидаемая итоговая стоимость
        """
        with allure.step(f'Проверка, что Итого с НДС внизу корзины равна {expected_total_price}'):
            self._total_price.should_float_value_in_element(expected_value=expected_total_price)

    def check_total_amount_cart(self, article_list: list[str]) -> None:
        """
        Проверяем, что итоговая сумма посчитана верно (которая отображается внизу корзины).
        Берем сумму Итого с НДС всех артикулов и сравниваем с итогоой суммой
        :param article_list: Список артикулов в корзине
        """
        with allure.step('Проверяем, что итоговая сумма посчитана верно (которая отображается внизу корзины)'):
            list_price_with_nds = []
            for el in article_list:
                list_price_with_nds.append(
                    self._list_material_component.save_total_price_with_nds_by_article(article=el))

            summ_price_with_nds_all_article = round(sum(list_price_with_nds), 2)
            print(summ_price_with_nds_all_article)

            footer_total_price_cart = self._total_price.get_float_value_from_line()
            assertions.assert_eq(
                actual_value=footer_total_price_cart,
                expected_value=summ_price_with_nds_all_article,
                allure_title='Сверяем сумму цены с НДС по каждой линии со стоимостью Итого с НДС внизу корзины',
                error_message=f'Стоимость Итого с НДС внизу корзины не соответствует сумме цен с НДС по каждой линии. '
                              f'Сумма по каждой линии - {summ_price_with_nds_all_article}; Итого с НДС внизу корзины - {footer_total_price_cart}'
            )

    def check_currency_in_total_price_footer(self, expected_currency: str) -> None:
        """Проверка валюты итоговой стоимости в футере корзины (внизу под списком кодов)"""
        with allure.step(
                f'Проверка, что валюта итоговой стоимости в футере корзины (под списком кодов) - {expected_currency}'):
            value_course = self._total_price.get_text_element()[-1]
            assertions.assert_eq(
                actual_value=value_course,
                expected_value=expected_currency,
                allure_title='Сверяем валюту итоговой стоимости в футере (под списком кодов) корзины с ожидаемым значением',
                error_message=f'Валюта итоговой стоимости в футере (под списком кодов) не соответствует ожидаемой. '
                              f'В тулбаре корзины - {value_course}; ожидаемое - {expected_currency}'
            )
