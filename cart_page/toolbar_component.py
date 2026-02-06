import allure
from selenium.webdriver.chrome.webdriver import WebDriver

from base_page.base_page import BasePage
from components.base_component import BaseComponent
from components.open_components.loader_component import LoaderComponent
from components.open_components.modal_add_zip_and_insulation import ModalAddZipAndInsulation
from components.open_components.modal_equipment_cost_calculation import ModalEquipmentCostCalculation
from elements.button import Button
from elements.li import Li
from elements.radio_button import RadioButton
from elements.text import Text
from elements.ul_list import UlList
from tools.validators import assertions


class ToolbarComponent(BaseComponent):
    """
    Тулбар корзины
    Скриншот компонента: docs/images_component_open/cart_components/toolbar_cart_component.png
    """

    NAME_PAGE = '|Корзина|'

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

        # Компоненты
        self.modal_add_zip_and_insulation = ModalAddZipAndInsulation(driver)
        self._modal_equipment_cost_calculation = ModalEquipmentCostCalculation(driver)
        self._loader_component = LoaderComponent(driver)
        self._page_base = BasePage(driver)

        # Text
        self._header_cart_is_empty = Text(driver, "//h2[contains(text(), 'Корзина пуста')]", "Заголовок Корзина пуста")
        self._price_total_in_toolbar = Text(
            driver,
            "//div[@data-name='list-toolbar-goods']//div[@data-id='cart-total-price-block']//span[text()]",
            "Итоговая стоимость. В тулбаре (сверху)")
        self._selected_payment_mode = Text(
            driver,
            "//div[@data-id='cart-payments-single-select-title']//span[text()]",
            "Выбранный режим оплаты")
        self._selected_course = Text(driver,
                                     "//input[@name='currencyName']/parent::label[contains(@class, 'btn-danger')]//span[text()]",
                                     "Выбранный курс")

        # button
        self._btn_update_cart = Button(driver, "//button[@data-id='cart-refresh-btn']", "Обновить корзину")
        self._btn_empty_trash = Button(driver, "//button[@data-id='cart-clean-btn']", "Очистить корзину")
        self._btn_add_zip = Button(driver, "//button[@data-id='cart-zip-active-btn']", "+ ЗИП и изоляция")
        self._btn_unload = Button(driver, "//button[@data-id='cart-unload-list-btn']", "Выгрузить")
        self._btn_save_in_excel = Button(driver, "//button[@data-id='cart-unload-list-excel-btn']", "Сохранить в Excel")
        self._btn_cost_calculation = Button(driver, "//button[@data-id='cart-unload-list-calculate-btn']",
                                            "Расчет стоимости")
        self._btn_switch_to_ue_course = Button(driver, "//input[@value='conventional unit']/parent::label",
                                               "Переключение курса на У.Е.")
        self._btn_open_closed_ul_payment_mode = Button(
            driver,
            "//div[@data-id='cart-payments-single-select-title']/div[@class='single-select__value-title-icon']",
            "Открыть/Закрыть выпадающий список Режим оплаты")

        # radio button
        self._radio_button_hidden_ue_course = RadioButton(driver, "//input[@value='conventional unit']", "Курс УЕ")
        self._radio_button_currency = RadioButton(driver, "//input[@name='currencyName']",
                                                  "Курс. Скрытый input типа radio")

        # ul
        self._values_in_ul_payment_mode = UlList(
            driver,
            "//ul[@data-id='cart-payments-single-select-box']//li//span[text()]",
            "Значения в выпадающем списке Режим оплаты")

        # li
        self._item_ul_payment_mode_by_payment_mode = Li(
            driver,
            "//ul[@data-id='cart-payments-single-select-box']//span[normalize-space(text())='{payment_mode}']",
            "Режим оплаты")

    def should_payment_mode(self, expected_payment_mode: str) -> None:
        """
        Должен быть выбран определенный Режим оплаты
        :param expected_payment_mode: Ожидаемый выбранный Режим оплаты
        """
        with allure.step(f'Проверка, что Режим оплаты выбран- {expected_payment_mode}'):
            self._selected_payment_mode.should_text_in_element(expected_text=expected_payment_mode)

    def should_items_in_ul_payment_mode(self, expected_list_payment_mode: list[str]) -> None:
        """
        Должны быть определенные значения в выпадающем списке Режим оплаты
        :param expected_list_payment_mode: Ожидаемые значения в выпадающем списке Режим оплаты
        """
        with allure.step(f'Проверка, что в выпадающем списке Режим оплаты есть значения- {expected_list_payment_mode}'):
            self._values_in_ul_payment_mode.should_value_in_ul(expected_values_in_ul=expected_list_payment_mode)

    def choice_payment_mode(self, payment_mode: str) -> None:
        """
        Выбор режима оплаты
        :param payment_mode: Режим оплаты для выбора
        """
        with allure.step(f'{self.NAME_PAGE} Выбор режима оплаты {payment_mode}'):
            self._btn_open_closed_ul_payment_mode.scroll_to_elem_action_chains()
            self._btn_open_closed_ul_payment_mode.click()
            self._item_ul_payment_mode_by_payment_mode.wait_visible_on_page(payment_mode=payment_mode)
            self._item_ul_payment_mode_by_payment_mode.click(payment_mode=payment_mode)
            self._loader_component.waiting_for_loader_no_text_processing_on_page()
            self.should_payment_mode(expected_payment_mode=payment_mode)

    def click_button_update_cart(self) -> None:
        """Клик по кнопке обновить корзину"""
        with allure.step('Клик по кнопке обновить корзину'):
            self._btn_update_cart.click()
            self._loader_component.waiting_for_loader_no_text_processing_on_page(timeout=20)
            self._loader_component.waiting_for_loader_no_text_processing_on_page(timeout=20)

    def click_empty_trash(self) -> None:
        """Клик по кнопке Очистить корзину, если корзина не пустая"""
        with allure.step('Клик по кнопке Очистить корзину, если корзина не пустая'):
            self._loader_component.waiting_for_loader_no_text_processing_on_page()
            self._loader_component.waiting_for_loader_text_processing_on_page()

            is_btn_empty_trash = self._btn_empty_trash.find_elements_safely()

            if is_btn_empty_trash:
                self._btn_empty_trash.click()
                self._loader_component.waiting_for_loader_no_text_processing_on_page()
                self._header_cart_is_empty.wait_visible_on_page()

    def add_zip(self, article: str) -> None:
        """
        Добавление ЗИП
        :param article: Наименование артикула
        """
        with allure.step(f'Добавление ЗИП по артикулу {article}'):
            self._btn_add_zip.click()
            self._loader_component.waiting_for_loader_no_text_processing_on_page()
            self.modal_add_zip_and_insulation.should_header()
            self.modal_add_zip_and_insulation.select_check_box_zip_by_article(article=article)
            self.modal_add_zip_and_insulation.click_btn_add_to_cart()

    def click_btn_upload(self) -> None:
        """Нажать на кнопку 'Выгрузить'"""
        with allure.step('Клик по кнопке Выгрузить в корзине'):
            self._btn_unload.click()
            self._btn_save_in_excel.wait_visible_on_page()

    def save_in_excel(self, num_contract: str = 'RT25-7705238125-HE', is_cart_rol: bool = False) -> None:
        """
        Нажать на кнопку Выгрузить в Excel
        :param num_contract: Номер договора клиента
        :param is_cart_rol: Корзина РОЛ или не РОЛ (если корзина РОЛ, то имя файла одно, если корзина дистра, то имя файла другое)
        """
        with allure.step('Клик по кнопке Выгрузить в Excel в корине'):
            # есл корзина РОЛ (непрямого клиента), то имя ожидаемого файла одно
            if is_cart_rol:
                name_file = 'cart_rol.xlsx'
            else:
                name_file = f'cart_{num_contract}.xlsx'

            self._page_base.delete_file_by_name_in_download_folder(name_file)
            self._btn_save_in_excel.click()
            self._loader_component.waiting_for_loader_no_text_processing_on_page()
            self._page_base.checking_the_download_document_in_the_download_folder(name_file)
            self._page_base.delete_file_by_name_in_download_folder(name_file)

    def click_btn_cost_calculation(self) -> None:
        """Нажать на кнопку Расчет стоимости"""
        with allure.step('Клик по кнопке Расчет стоимости'):
            self._btn_cost_calculation.click()
            self._modal_equipment_cost_calculation.should_header()

    def click_button_switch_to_ue(self) -> None:
        """Клик по кнопке Переключить курс на уе"""
        with allure.step('Переключение курса на УЕ'):
            self._btn_switch_to_ue_course.click()
            self._loader_component.waiting_for_loader_no_text_processing_on_page()
            self._radio_button_hidden_ue_course.radio_button_should_selected()

    def check_count_currency_to_choose(self, expected_count_icon_currency: int) -> None:
        """
        Проверяем доступное количество курсов для выбора
        :param expected_count_icon_currency: Ожидаемое доступное количество курсов для выбора
        """
        with allure.step(f'Проверка, что доступно для выбора курса доступно {expected_count_icon_currency} вида курса'):
            count_curse = len(self._radio_button_currency.find_elements_safely())
            assertions.assert_eq(
                actual_value=count_curse,
                expected_value=expected_count_icon_currency,
                allure_title='Проверяем, что на странице есть только одна кнопка выбора курса.',
                error_message=f'На странице больше 1 - ой кнопки для переключения курса. Количество - {count_curse}'
            )

    def check_selected_course(self, expected_course: str) -> None:
        """
        Проверка выбранного курса
        :param expected_course: Ожидаемый выбранный курс
        """
        with allure.step(f'Проверка, что выбран курс {expected_course}'):
            selected_course = self._selected_course.get_text_element()

            assertions.assert_eq(
                actual_value=selected_course,
                expected_value=expected_course,
                allure_title='Смотрим значение в выбранном курсе',
                error_message=f'Выбранный курс в корзине не соответствует ожидаемому. '
                              f'В корзине - {selected_course}, ожидаемый - {expected_course}'
            )

    def save_total_with_nds(self) -> float:
        """Сохранение значения в поле Итого с НДС"""
        with allure.step('Тулбар корзины. Сохранение значения Итого с НДС'):
            return self._price_total_in_toolbar.get_float_value_from_line()

    def check_currency_in_total_price_toolbar(self, expected_currency: str) -> None:
        """Проверка валюты итоговой стоимости в тулбаре"""
        with allure.step(
                f'Проверка, что валюта итоговой стоимости в тулбаре корзины - {expected_currency}'):
            value_course = self._price_total_in_toolbar.get_text_element()[-1]
            assertions.assert_eq(
                actual_value=value_course,
                expected_value=expected_currency,
                allure_title='Сверяем валюту итоговой стоимости в тулбаре корзины с ожидаемым значением',
                error_message=f'Валюта итоговой стоимости в тулбаре не соответствует ожидаемой. '
                              f'В тулбаре корзины - {value_course}; ожидаемое - {expected_currency}'
            )
