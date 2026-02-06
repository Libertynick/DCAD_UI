import allure
from selenium.webdriver.chrome.webdriver import WebDriver

from components.base_component import BaseComponent
from components.open_components.loader_component import LoaderComponent
from components.open_components.tooltip_composition_of_set_component import TooltipCompositionOfSetComponent
from elements.button import Button
from elements.input import Input
from elements.text import Text
from open_pages.cart_page.toolbar_component import ToolbarComponent
from tools.validators import assertions


class ListArticleComponent(BaseComponent):
    """
    Компонент Список артикулов в корзине
    Скриншот компонента: docs/images_component_open/cart_components/list_article_component.png
    """

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

        self.loader_open = LoaderComponent(driver)
        self._toolbar_component_cart = ToolbarComponent(driver)
        self.tooltip_composition_of_set_component = TooltipCompositionOfSetComponent(driver)

        # button
        self._btn_edit_article = Button(driver, "//button[contains(text(), 'Редактировать')]", "Редактировать артикул")
        self._btn_save_when_editing = Button(
            driver,
            "//button[contains(text(), 'Сохранить') and @class='btn text-primary shadow-none']",
            "Сохранить (при редактировании артикула)")
        self._btn_tooltip_article = Button(driver, "//i[@class='bi bi-exclamation-circle text-danger small']",
                                           "Тултип у артикула")
        self._btn_icon_promo_curse_by_article = Button(
            driver,
            "//span[contains(text(), '{article}')]/ancestor::div[contains(@class, 'row')]//div[@data-id='cart-special-promo-tooltip']",
            "Иконка промо курса по артикулу")
        self._btn_icon_internal_course_by_article = Button(
            driver,
            "//span[contains(text(), '{article}')]/ancestor::div[contains(@class, 'row')]//div[@data-id='cart-special-nopromo-tooltip']",
            "Иконка внутреннего курса у артикула (не промо курса)")
        self._btn_tooltip_special_price_by_article = Button(
            driver,
            "//a[@data-id='cart-list-item-link']/span[contains(text(), '{article}')]/following::div[@data-id='cart-special-price-tooltip']//i",
            "Тултип спец цены по артикулу")
        self._btn_icon_direction_by_article = Text(
            driver,
            "//span[normalize-space(text())='{article}']/ancestor::div[contains(@class, 'goods-list-item')]//div[contains(@class, 'gap-2')]/div[@data-popper-container]//span[@data-chosen-icon]",
            "Иконка направления отдела по артикулу")

        # Text
        self._header_column_price_list = Text(driver,
                                              "//span[normalize-space(text())='Прайс-лист,']/parent::div/span/span",
                                              "Заголовок колонки Прайс Лист")
        self._header_column_total = Text(driver, "//span[normalize-space(text())='Итого,']/parent::div/span/span",
                                         "Заголовок колонки Итого")
        self._header_column_with_nds = Text(driver, "//span[normalize-space(text())='с НДС,']/parent::div/span/span",
                                            "Заголовок колонки с НДС,")
        self._code_name = Text(
            driver,
            "//span[@class='col-4 d-flex flex-column flex-sm-row align-items-center py-lg-2 pe-lg-1']//span[text()][2]",
            "Наименование Кода/артикула")
        self._name_article_by_article = Text(
            driver, "//*[contains(text(), '{article}') or contains(text(), '{article}R')]",
            "Наименование артикула по определенному ({article}) артикулу")
        self._autocorrect_old_code = Text(driver, "//div[@class='px-2 bg-whisper-light text-decoration-line-through']",
                                          "Наименование старого кода при автозамене")
        self._autocorrect_new_code = Text(
            driver,
            "//div[text()=' Замена материала ']/preceding-sibling::div[@class='px-2 ms-2 text-gray-dark bg-green-light']",
            "Наименование нового кода при автозамене")
        self._autocorrect_code = Text(
            driver, "//div[text()='{article}']/following-sibling::div[text()=' Замена материала ']",
            "Автозамена артикула")
        self._product_delivery_completion_message_by_article = Text(
            driver,
            "//span[contains(text(), '{article}')]/ancestor::div[contains(@class, 'border-end-0 bg-pink')]//div[@class='response-box']",
            "Сообщение о завершении поставок продукта")
        self._description_by_article = Text(
            driver,
            "//span[contains(text(), '{article}')]/ancestor::div[@class='']//span[@class='goods-list-item-card__name text-break']",
            "Описание по артикулу")
        self._price_list_by_article = Text(driver,
                                           "//span[text()='{article}']/ancestor::div[contains(@class, 'row')][last()]/div[2]//span",
                                           "Прайс-лист по артикулу")
        self._total_with_nds_by_article = Text(
            driver,
            "//span[text()='{article}']/ancestor::div[contains(@class, 'row')][last()]//div[@class='col-4']",
            "Итого с НДС по артикулу")
        self._in_stock_by_article = Text(driver,
                                         "//span[text()='{article}']/ancestor::div[contains(@class, 'row')][last()]//span[@class='fw-bold text-success']",
                                         "Количество на складе по артикулу")
        self._allowance_article = Text(driver, "//div[@class='col-5 py-2']//div[@class='col-6' and contains(., '%')]",
                                       "Надбавка артикула")
        self._text_in_tooltip_promo_curse_by_article = Text(
            driver,
            "//span[contains(text(), '{article}')]/ancestor::div[contains(@class, 'row')]//div[@data-id='cart-special-promo-tooltip']//div[@class='text-wrap']",
            "Информация в тултипе промо курса по артикулу")
        self._text_in_tooltip_internal_course_by_article = Text(
            driver,
            "//span[contains(text(), '{article}')]/ancestor::div[contains(@class, 'row')]//div[@data-id='cart-special-nopromo-tooltip']//div[@class='text-wrap']",
            "Информация в тултипе внутреннего курса по артикулу (не промо курс)")
        self._message_tooltip_special_price_by_article = Text(
            driver,
            "//a[@data-id='cart-list-item-link']/span[contains(text(), '{article}')]/following::div[@class='text-wrap']",
            "Информация в тултипе спец цены по артикулу")
        self._discount = Text(driver, "//div[@class='col-5 py-2']//div[@class='col-2']", "Скидка")

        # input
        self._input_amount_by_article = Input(
            driver,
            "//span[contains(text(), '{article}')]/ancestor::div[@class='']//input[contains(@class, 'py-1 px-2 rounded')]",
            "Количество штук по артикулу")
        self._input_amount = Input(driver, "//input[@data-id='cart-quantity-item-input']", "Количество штук")
        self._input_article_when_editing = Input(
            driver, "//span[contains(text(), '№/Код')]/following-sibling::input", "Артикул при редактировании")
        self._input_amount_when_editing = Input(
            driver, "//span[contains(text(), 'Кол-во, шт.')]/following-sibling::input",
            "Количество при редактировании артикула")

    def click_btn_edit(self) -> None:
        """Клик по кнопке Редактировать у артикула"""
        with allure.step('Клик по кнопке Редактировать у артикула'):
            self._btn_edit_article.click()
            self._btn_save_when_editing.wait_visible_on_page()

    def should_price_list_column_currency(self, expected_currency: str) -> None:
        """
        Должна быть определенная валюта в колонке Прайс лист
        :param expected_currency: Ожидаемая валюта
        """
        with allure.step(f'Проверяем, что в колонке Прайс лист валюта - {expected_currency}'):
            self._header_column_price_list.should_text_in_element(expected_text=expected_currency)

    def should_total_column_currency(self, expected_currency: str) -> None:
        """
        Должна быть определенная валюта в колонке Итого
        :param expected_currency: Ожидаемая валюта
        """
        with allure.step(f'Проверяем, что в колонке Итого валюта - {expected_currency}'):
            self._header_column_total.should_text_in_element(expected_text=expected_currency)

    def should_with_nds_column_currency(self, expected_currency: str) -> None:
        """
        Должна быть определенная валюта в колонке С НДС
        :param expected_currency: Ожидаемая валюта
        """
        with allure.step(f'Проверяем, что в колонке с НДС валюта - {expected_currency}'):
            self._header_column_with_nds.should_text_in_element(expected_text=expected_currency)

    def save_list_articles_in_cart(self) -> list:
        """Сохранение списка артикулов в корзине"""
        with allure.step('Сохранение списка артикулов в корзине'):
            self._code_name.wait_visible_on_page()
            name_codes_link_in_cart = self._code_name.get_text_list_element()
            return name_codes_link_in_cart

    def save_description_by_article(self, article: str) -> str:
        """
        Сохранение описания по артикулу
        :param article: Наименование артикула
        :return: Описание артикула
        """
        with allure.step(f'Сохранение описания артикула {article}'):
            return self._description_by_article.get_text_element(article=article)

    def checking_adding_items_to_cart(self, article_list_expected: list) -> None:
        """
        Проверка добавления кодов в корзину
        :param article_list_expected: Список ожидаемых артикулов. Должен подаваться без количества. Например: 015P1001 082X9019 065B8316RG
        """
        with allure.step(f'Проверка добавления кодов в корзину. expected - {article_list_expected}'):
            article_list_on_page = self.save_list_articles_in_cart()

            # Смотрим есть ли автозамена в корзине. Если есть, то заменяем артикулы в ожидаемом списке
            for idx, article in enumerate(article_list_expected):
                autocorrect_code_list = self.check_if_there_is_code_autocorrect(article)
                article_list_expected[idx] = autocorrect_code_list[1] if len(autocorrect_code_list) != 0 else article

            assertions.assert_eq(
                actual_value=article_list_on_page,
                expected_value=article_list_expected,
                allure_title='Сверяем коды в корзине с ожидаемыми',
                error_message=f'Список артикулов в корзине не соответствует ожидаемому. '
                              f'В корзине- ({article_list_on_page}); ожидаемый- ({article_list_expected})'
            )

    def check_if_there_is_code_autocorrect(self, article: str) -> list:
        """
        Проверка есть ли автозамена
        :param article: Артикул, у которого проверяем автозамену
        :return: Список артикулов. [old_article, new_article]; old_article - старый код, который заменили;
        new_article- новый код, на который заменили. В случае, если нет автозамены, возвращаем пустой список
        """
        with allure.step(f'Проверка есть ли автозамена по артикулу {article}'):
            old_new_codes = []
            self._name_article_by_article.wait_visible_on_page(timeout=5, article=article)
            autocorrect = self._autocorrect_code.find_elements_safely(article=article)
            if len(autocorrect) > 0:
                old_code = self._autocorrect_old_code.get_text_element()
                old_new_codes.append(old_code)
                new_code = self._autocorrect_new_code.get_text_element()
                old_new_codes.append(new_code)
            return old_new_codes

    def save_article_edit(self, article_for_edit: str) -> None:
        """Сохранение редактирования артикула
        article_for_edit - код для редактирования (который должен отображаться в корзине)
        """
        with allure.step(f'Сохранение и проверка редактирования артикула {article_for_edit}'):
            self._btn_save_when_editing.click()
            self._btn_edit_article.wait_visible_on_page()

            self._toolbar_component_cart.click_button_update_cart()
            self.loader_open.waiting_for_loader_text_processing_on_page()
            article_in_cart = self.save_list_articles_in_cart()

            autocorrect_code = self.check_if_there_is_code_autocorrect(article_for_edit)
            autocorrect_code = autocorrect_code[1] if len(autocorrect_code) != 0 else ''
            article_for_edit = autocorrect_code if len(autocorrect_code) != 0 else article_for_edit

            assertions.assert_contains(
                actual_value=article_in_cart,
                expected_contains=article_for_edit,
                allure_title='Смотрим есть ли код после редактирования в корзине',
                error_message=f'Код для редактирования не отображается в корзине после редактирования. '
                              f'Код для редактирования- {article_for_edit}; список кодов в корзине- ({article_in_cart})'
            )

    def check_count_article(self, expected_list_article_with_count: list[str]) -> None:
        """
        Проверка количества штук у списка артикулов в корзине
        :param expected_list_article_with_count: Ожидаемый список артикулов с количеством. Пример: ['160W2996R 1', '003Z1813RF 25', '003Z1064R 3']
        """
        with allure.step(
                f'Проверка количества штук у списка артикулов в корзине. Ожидаем: {expected_list_article_with_count}'):
            expected_dict = {}

            for el in expected_list_article_with_count:
                key, value = el.rsplit(' ', 1)  # разделяем по последнему пробелу
                expected_dict[key] = value

            article_in_cart = self._code_name.get_text_list_element()
            for el in article_in_cart:
                count_in_cart = self._input_amount_by_article.get_value(article=el)
                expected_count = expected_dict[el]
                assertions.assert_eq(
                    actual_value=count_in_cart,
                    expected_value=expected_count,
                    allure_title=f'Проверка количества по коду {el}',
                    error_message=f'Количество у кода {el} в корзине не соответствует ожидаемому. '
                                  f'В корзине - {count_in_cart}, ожидаемое - {expected_count}'
                )

    def enter_the_number_of_pieces_in_the_quantity_input_field(self, amount: int) -> None:
        """Ввод количество штук в поле ввода Количество штук"""
        with allure.step(f'Ввод количество штук {amount} в поле ввода Количество штук'):
            self._input_amount.wait_visible_on_page().clear()
            self._input_amount.filling_input(amount)
            self._input_amount.should_value_in_input_field(amount)

    def save_amount_product_by_article(self, article: str) -> str:
        """Сохранение количества штук по артикулу"""
        with allure.step(f'Сохранение количества штук по артикулу {article}'):
            amount_product = self._input_amount_by_article.get_value(article=article)
            return amount_product

    def checking_product_delivery_completion_message(self, article: str) -> None:
        """Проверка сообщения о завершении поставок продукта"""
        with allure.step(f'Проверка сообщения о завершении поставок продукта по артикулу - ({article})'):
            expected_message = 'Уточните возможность поставки аналогичного продукта у сотрудников технической поддержки'

            self._product_delivery_completion_message_by_article.should_text_in_element(expected_text=expected_message,
                                                                                        article=article)

    def entering_an_article_when_editing(self, article: str) -> None:
        """Ввод артикула при редактировании артикула"""
        with allure.step(f'Ввод артикула ({article}) при редактировании артикула'):
            self._input_article_when_editing.clear_input()
            self._input_article_when_editing.filling_input(article)

    def entering_an_amount_when_editing(self, amount: int) -> None:
        """Ввод количество при редактировании артикула"""
        with allure.step(f'Ввод количества {amount} при редактировании артикула'):
            self._input_amount_when_editing.clear_input()
            self._input_amount_when_editing.filling_input(amount)

    def click_toolip_article(self) -> None:
        """Клик по тултипу у артикула"""
        with allure.step('Клик по тултипу у артикула в корзине'):
            self._btn_tooltip_article.click(timeout=3)
            self.tooltip_composition_of_set_component.should_header()

    def save_price_list_by_article(self, article: str) -> float:
        """
        Сохранение прайс-листа по артикулу
        :param article: Наименование артикула
        :return: Значение прайс-листа по артикулу
        """
        with allure.step(f'Сохранение прайс-листа по артикулу ({article})'):
            return self._price_list_by_article.get_float_value_from_line(article=article)

    def checking_whether_payment_is_being_made_at_promotional_rate(self, article: str,
                                                                   price_list_article_rub: float) -> None:
        """Проверка идет ли расчет с рублей в УЕ по промо курсу
        price_list_article_rub - прайс-лист артикула в рублях
        """
        with allure.step(f'Проверка идет ли расчет с рублей в уе по промо курсу артикула {article}'):
            promo_curse = 115

            expected_price_list_by_promo_curse_ue = round(price_list_article_rub / promo_curse,
                                                          2)  # прайс-лист в уе, рассчитанный по промо курсу (ожидаемый)

            price_list_on_page = self.save_price_list_by_article(article)  # Прайс-лист в уе на странице

            assertions.assert_eq(
                actual_value=price_list_on_page,
                expected_value=expected_price_list_by_promo_curse_ue,
                allure_title='Сравниваем прайс-лист артикула с прайсом по промо курсу',
                error_message=f'Прайс-лист артикула {article} в корзине не соответствует прайсу по промо курсу. '
                              f'Прайс-лист артикула- {price_list_on_page}; прайс-лист по промо курсу- {expected_price_list_by_promo_curse_ue}'
            )

    def store_quantity_in_stock(self, article: str) -> int:
        """
        Сохранение количества на складе одного артикула
        :param article: Наименование артикула
        :return: Количество на складе
        """
        with allure.step(f'Сохранение количества на складе по артикулу ({article})'):
            quantity_in_stock = self._in_stock_by_article.find_elements_safely(article=article)
            if len(quantity_in_stock) != 0:
                quantity_in_stock = quantity_in_stock[0].text
                return int(quantity_in_stock)
            else:
                return 0

    def save_allowances(self) -> list[float]:
        """Сохранение всех надбавок"""
        with allure.step('Сохранение всех надбавок в корзине'):
            return self._allowance_article.get_float_value_from_all_line()

    def there_must_be_a_prom_curse_for_article(self, article: str) -> None:
        """Должен быть промо курс у артикула"""
        with allure.step(f'Проверка отображения иконки промо курса у артикула {article}'):
            expected_text_in_tooltip_promo_curse = 'Специальное правило расчёта. Применён курс 115 руб., при расчёте стоимости по прайсу.'

            self._btn_icon_promo_curse_by_article.scroll_to_elem_action_chains(article=article)
            self._btn_icon_promo_curse_by_article.click(article=article)
            self._text_in_tooltip_promo_curse_by_article.wait_visible_on_page(article=article)
            self._text_in_tooltip_promo_curse_by_article.should_text_in_element(
                expected_text=expected_text_in_tooltip_promo_curse, article=article)

    def there_must_be_a_internal_curse_by_article(self, article: str) -> None:
        """Должен быть внутренний курс у артикула"""
        with allure.step(f'Проверка отображения иконки внутреннего курса у артикула {article}'):
            expected_text = 'Рассчитано по курсу: у.е.'  # В конце есть значение курса, проверяем без него

            self._btn_icon_internal_course_by_article.scroll_to_elem_action_chains(article=article)
            self._btn_icon_internal_course_by_article.click(article=article)
            self._text_in_tooltip_internal_course_by_article.wait_visible_on_page(article=article)

            text_in_tooltip_internal_curse = self._text_in_tooltip_internal_course_by_article.get_text_element(
                article=article).split(' ')[:-1]
            text_in_tooltip_internal_curse = ' '.join(text_in_tooltip_internal_curse)

            assertions.assert_eq(
                actual_value=text_in_tooltip_internal_curse,
                expected_value=expected_text,
                allure_title='Сверяем текст в тултипе с ожидаемым. В конце есть значение курса, проверяем без него',
                error_message=f'У артикула {article} текст в тултипе внутреннего курса не соответствует ожидаемому.'
                              f' Текст в тултипе- {text_in_tooltip_internal_curse}; ожидаемый- {expected_text}'
            )

    def check_special_price_info_in_list_article(self, article_list: list[str]) -> None:
        """Проверка, что у кодов в списке артикулов есть информация о спец цене (в виде тултипа)"""
        with allure.step('Проверка, что у кодов в списке артикулов есть информация о спец цене (в виде тултипа)'):
            expected_text_in_tooltip_special_price = 'Специальная цена'  # Ожидаемый текст в тултипе спец цены

            for article in article_list:
                self._btn_tooltip_special_price_by_article.scroll_to_elem_action_chains(article=article)
                self._btn_tooltip_special_price_by_article.click(article=article)
                self._message_tooltip_special_price_by_article.wait_visible_on_page(article=article)
                self._message_tooltip_special_price_by_article.should_text_in_element(article=article,
                                                                                      expected_text=expected_text_in_tooltip_special_price)

    def store_discounts_all_articles(self) -> list[float]:
        """Сохранение скидок у всех артикулов"""
        with allure.step('Сохранение скидок у всех артикулов'):
            return self._discount.get_float_value_from_all_line()

    def check_that_each_item_has_department_direction_icon(self, article_list: list[str]) -> None:
        """
        Проверяем, что в каждом артикуле присутствует иконка направления отдела
        :param article_list: Список артикулов для проверки
        """
        with allure.step('Проверяем, что в каждом артикуле присутствует иконка направления отдела'):
            for el in article_list:
                icon_direction = len(self._btn_icon_direction_by_article.find_elements_safely(article=el))
                assertions.assert_not_eq(
                    actual_value=icon_direction,
                    value_not_eq=0,
                    allure_title='Проверка, что есть иконки направления на странице',
                    error_message=f'У артикула {el} не отображается иконка направления отдела. Количество - {icon_direction}'
                )

    def save_total_price_with_nds_by_article(self, article: str) -> float:
        """
        Сохранение Итого с НДС по артикулу
        :param article: Наименование артикула
        :return: Итого с НДС по артикулу
        """
        with allure.step(f'Сохранение Итого с НДС артикула {article}'):
            return self._total_with_nds_by_article.get_float_value_from_line(article=article)
