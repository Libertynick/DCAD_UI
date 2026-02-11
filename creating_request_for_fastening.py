import re
import time

import allure
from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver

from base_page.base_page import BasePage
from base_page.base_page_locators import BaseOpenLocators
from elements.button import Button
from elements.check_box import CheckBox
from elements.input import Input
from elements.li import Li
from elements.radio_button import RadioButton
from elements.text import Text
from elements.ul_list import UlList
from open_pages.fastening_request.additional_distributor_data_component import AdditionalDistributorDataComponent
from open_pages.objects_page.fastening_requests_list.locators_fastening_requests_list import \
    CreatingRequestForFasteningLocators, FasteningRequestsListLocators, ModalNumberOfYourApplicationLocators


@allure.feature('Создание заявки на крепление')
class CreatingRequestForFasteningPage(BasePage):
    """Страница Создание заявки на крепление"""

    def __init__(self, driver: WebDriver, url=''):
        super().__init__(driver, url)

        # компоненты
        self.additional_distributor_data_component = AdditionalDistributorDataComponent(driver)

        # Текстовые элементы
        self.header = Text(driver, "//h1[contains(text(), 'Создание заявки на крепление')]",
                           "Заголовок Создание заявки на крепление")
        self.header_specification = Text(
            driver,
            "//form[@id='save-application']//span[contains(text(), 'Спецификация')]",
            "Заголовок Спецификация")
        self.header_commercial_offer = Text(
            driver,
            "//form[@id='save-application']//span[contains(text(), 'Коммерческое предложение')]",
            "Заголовок Коммерческое предложение")
        self.header_participants_of_object = Text(driver, "//h5[contains(text(), 'Участники объекта')]",
                                                  "Заголовок Участники объекта")
        self.header_additional_information = Text(driver,
                                                  "//div[@class='col-12']/h5[contains(text(), 'Дополнительная информация')]",
                                                  "Заголовок Дополнительная информация")
        self.header_reason_for_application = Text(driver, "//h5[contains(text(), 'Основание для заявки')]",
                                                  "Заголовок Основание для заявки")
        self.selected_author_request = Text(
            driver,
            "//div[contains(text(), 'Автор заявки')]/following-sibling::div[@data-id='-single-select-title']//span[text()]",
            "Выбранное значение в поле Автор заявки")
        self.selected_inn_in_chapter_object = Text(
            driver,
            "//div[contains(text(), 'ИНН')]/following-sibling::div[@data-id='-single-select-title']//span[text()]",
            "Выбранный ИНН в разделе Объект")
        self.selected_sales_office = Text(
            driver,
            "//div[contains(text(), 'Офис продаж')]/following-sibling::div[1]//span[text()]",
            "Выбранный офис продаж в разделе Объект")
        self.selected_engineer_section = Text(
            driver,
            "//div[contains(text(), 'Инженерный раздел')]/parent::div//div[contains(@class, 'text-truncate')]/span",
            "Выбранный инженерный раздел в разделе Объект")
        self.selected_access_to_object_manager = Text(
            driver,
            "//div[contains(text(), 'Доступ')]/following-sibling::div[@data-id='-single-select-title']//span[@data-value-element]",
            "Выбранный доступ менеджеру объекта")
        self.section_close_additional_distributor_details = Text(
            driver,
            "//div[@id='collapse-distributor' and not(contains(@class, 'show'))]",
            "Закрытый раздел Дополнительные данные дистрибьютора")
        self.section_opened_additional_distributor_details = Text(
            driver,
            "//div[@id='collapse-distributor' and contains(@class, 'show')]",
            "Раскрытый раздел Дополнительные данные дистрибьютора")
        self.header_country_in_additional_distributor_details = Text(
            driver,
            "//div[@id='collapse-distributor' and contains(@class, 'show')]//div[@class='me-1 phone-form-element-countries']//div[contains(text(), 'Страна')]",
            "Заголовок Страна в поле выбора кода телефона. Раздел Дополнительные данные дистрибьютора")
        self.header_phone_in_additional_distributor_details = Text(
            driver,
            "//div[@id='collapse-distributor' and contains(@class, 'show')]//div[@class='phone-form-element__number-box w-100 rounded border']//span[contains(text(), 'Телефон')]",
            "Заголовок Телефон в поле выбора кода телефона. Раздел Дополнительные данные дистрибьютора")
        self.selected_code_country_in_additional_distributor_details = Text(
            driver,
            "//input[@name='distributor[additionalData][phone_country_id]']/following-sibling::div//div[@data-id='-single-select-title']//span[text()]",
            "Выбранное значение кода страны. Раздел Дополнительные данные дистрибьютора")
        self.message_warning_in_participants_of_object = Text(
            driver,
            "//h5[contains(text(), 'Участники объекта')]/parent::div/following-sibling::div/div[contains(@class, 'alert')]//span[text()]",
            "Предупреждение в разделе Участники объекта")
        self.opened_chapter_investor_customer = Text(
            driver,
            "//div[@id='collapse-customer' and contains(@class, 'show')]",
            "Открытый раздел Инвестор/Заказчик")
        self.selected_code_country_in_investor_customer = Text(
            driver,
            "//input[@name='customer[phone_country_id]']/following-sibling::div//div[@data-id='-single-select-title']//span[text()]",
            "Выбранное значение кода страны. Инвестор/Заказчик")
        self.opened_chapter_designer = Text(driver, "//div[@id='collapse-designer' and contains(@class, 'show')]",
                                            "Открытый раздел Проектировщик")
        self.selected_code_country_in_designer = Text(
            driver,
            "//input[@name='designer[phone_country_id]']/following-sibling::div//div[@data-id='-single-select-title']//span[text()]",
            "Выбранное значение кода страны. Раздел Проектировщик")
        self.opened_chapter_general_contractor = Text(
            driver,
            "//div[@id='collapse-generalContractor' and contains(@class, 'show')]",
            "Открытый раздел Генеральный подрядчик")
        self.selected_code_country_in_general_contractor = Text(
            driver,
            "//input[@name='generalContractor[phone_country_id]']/following-sibling::div//div[@data-id='-single-select-title']//span[text()]",
            "Выбранное значение кода страны. Раздел Генеральный подрядчик")
        self.opened_chapter_installer_contractor = Text(driver,
                                                        "//div[@id='collapse-installer' and contains(@class, 'show')]",
                                                        "Открытый раздел Монтажник/Подрядчик")
        self.selected_code_country_in_installer_contractor = Text(
            driver,
            "//input[@name='installer[phone_country_id]']/following-sibling::div//div[@data-id='-single-select-title']//span[text()]",
            "Выбранное значение кода страны. Раздел Монтажник/Подрядчик")
        self.header_additional_files = Text(driver, "//span[contains(text(), 'Дополнительные файлы')]",
                                            "Заголовок Дополнительные файлы")
        self.help_text_in_additional_files = Text(driver,
                                                  "//label[@data-check-validation='additionalInformation[files]']//small",
                                                  "Подсказка в Дополнительные файлы")

        # Чек-боксы
        self.check_box_enter_name_in_chapter_object = CheckBox(
            driver,
            "//div[@class='row gy-3 mt-4 mb-4']//span[contains(text(), 'Ввести название самостоятельно')]/preceding-sibling::input[@type='checkbox']",
            "Ввести название самостоятельно в разделе Объект")
        self.check_box_enter_name_investor_customer = CheckBox(
            driver,
            "//div[@id='collapse-customer']//span[contains(text(), 'Ввести название самостоятельно')]/preceding-sibling::input[@type='checkbox']",
            "Ввести название самостоятельно. Инвестор/Заказчик")
        self.check_box_enter_name_designer = CheckBox(
            driver,
            "//div[@id='collapse-designer']//span[contains(text(), 'Ввести название самостоятельно')]/preceding-sibling::input[@type='checkbox']",
            "Ввести название самостоятельно. Раздел Проектировщик")
        self.check_box_enter_name_general_contractor = CheckBox(
            driver,
            "//div[@id='collapse-generalContractor']//span[contains(text(), 'Ввести название самостоятельно')]/preceding-sibling::input[@type='checkbox']",
            "Ввести название самостоятельно. Раздел Генеральный подрядчик")
        self.check_box_enter_name_installer_contractor = CheckBox(
            driver,
            "//div[@id='collapse-installer']//span[contains(text(), 'Ввести название самостоятельно')]/preceding-sibling::input[@type='checkbox']",
            "Ввести название самостоятельно. Раздел Монтажник/Подрядчик")

        # Radio button
        self.radio_button_is_purchaser = RadioButton(
            driver,
            "//input[@name='customer[isBuyer]']",
            "Является закупщиком. Инвестор/Заказчик")
        self.radio_button_is_general_contractor = RadioButton(
            driver,
            "//input[@name='generalContractor[isBuyer]']",
            "Является закупщиком. Генеральный подрядчик")
        self.radio_button_is_installer_contractor = RadioButton(
            driver,
            "//input[@name='installer[isBuyer]']",
            "Является закупщиком. Монтажник/Подрядчик")

        # Выпадающие списки
        self.active_ul_engineering_section = UlList(
            driver,
            "//div[contains(text(), 'Инженерный раздел')]/parent::div/div[contains(@class, 'active')]/ul",
            "Активированный список Инженерный раздел")
        self.active_ul_access_to_object_manager = UlList(
            driver,
            "//div[contains(text(), 'Доступ')]/following-sibling::div[contains(@class, 'active')][2]/ul",
            "Активированный список Доступ менеджеру объекта")

        # Элементы в выпадающем списке
        self.ul_item_sales_office = Li(
            driver,
            "//div[contains(text(), 'Офис продаж')]/following-sibling::div/ul/li",
            "Офис продаж в разделе Объект")
        self.ul_item_market = Li(
            driver,
            "//div[contains(text(), 'Рынок')]/following-sibling::div/ul/li",
            "Рынок в разделе Объект")
        self.ul_item_access_to_object_manager = Li(
            driver,
            "//div[contains(text(), 'Доступ')]/following-sibling::div[contains(@class, 'active')][2]/ul//span[text()]",
            "Доступ менеджеру объекта")
        self.ul_item_in_name_or_inn_company_investor_customer = Li(
            driver,
            "//div[@id='collapse-customer']//ul[contains(@class, 'active')]//span[text()]",
            "Название или ИНН компании в разделе Инвестор/Заказчик")
        self.ul_item_name_or_inn_company_general_contractor = Li(
            driver,
            "//div[@id='collapse-generalContractor']//ul[contains(@class, 'active')]//span[text()]",
            "Название или ИНН компании в разделе Генеральный подрядчик")

        # Кнопки
        self.btn_open_closed_ul_sales_office = Button(
            driver,
            "//div[contains(text(), 'Офис продаж')]/following-sibling::div[@data-id='-single-select-title']/div[@class='single-select__value-title-icon']",
            "Открыть - закрыть выпадающий список Офис продаж")
        self.btn_open_closed_ul_market = Button(
            driver,
            "//div[contains(text(), 'Рынок')]/following-sibling::div[@data-id='-single-select-title']/div[@class='single-select__value-title-icon']",
            "Открыть - закрыть выпадающий список Рынок")
        self.btn_open_closed_ul_engineering_section = Button(
            driver,
            "//input[@name='object[specType]']/preceding-sibling::div[@class='single-select__value-title-icon']",
            "Открыть - закрыть выпадающий список Инженерный раздел")
        self.btn_open_closed_ul_access_to_object_manager = Button(
            driver,
            "//div[contains(text(), 'Доступ')]/following-sibling::div[@data-id='-single-select-title']/div[@class='single-select__value-title-icon']",
            "Открыть - закрыть выпадающий список Доступ менеджеру объекта")
        self.btn_additional_distributor_details = Button(
            driver,
            "//button[@data-bs-target='#collapse-distributor']",
            "Дополнительные данные дистрибьютора")
        self.btn_open_closed_chapter_investor_customer = Button(
            driver,
            "//button[@data-bs-target='#collapse-customer']",
            "Открыть- закрыть раздел Инвестор/Заказчик")
        self.btn_open_closed_chapter_designer = Button(driver, "//button[@data-bs-target='#collapse-designer']",
                                                       "Открыть - закрыть раздел Проектировщик")
        self.btn_open_closed_chapter_general_contractor = Button(driver,
                                                                 "//button[@data-bs-target='#collapse-generalContractor']",
                                                                 "Открыть - закрыть раздел Генеральный подрядчик")
        self.btn_open_closed_chapter_installer_contractor = Button(driver,
                                                                   "//button[@data-bs-target='#collapse-installer']",
                                                                   "Открыть - закрыть раздел Монтажник/Подрядчик")
        self.btn_calendar_in_expected_delivery_date = Button(driver,
                                                             "//*[local-name()='svg' and @class='datepicker__decor-icon cursor-pointer']",
                                                             "Календарь. Ожидаемая дата поставки")
        self.btn_back = Button(driver,
                               "//a[@href='/cabinet/objects/applications-for-attachment' and contains(text(), 'Назад')]",
                               "Назад")
        self.btn_save_as_draft = Button(driver, "//button[contains(text(), 'Сохранить как черновик')]",
                                        "Сохранить как черновик ")
        self.btn_send = Button(driver, "//button[contains(text(), 'Отправить')]", "Отправить")

        # Поля ввода типа input
        self.input_address_in_object_chapter = Input(
            driver,
            "//input[@name='object[address]' and @form='save-application']", "Адрес в разделе Объект")
        self.input_specification = Input(driver, "//input[@id='specificationFiles']", "для загрузки спецификации")
        self.input_with_loaded_specification_files = Input(
            driver,
            "//input[@name='object[files][specifications][0]']",
            "с подгруженными файлами спецификации")
        self.input_commercial_offer = Input(
            driver,
            "//label[@data-check-validation='object[files][kp]']/following-sibling::input",
            "Коммерческое предложение")
        self.input_transaction_manager = Input(driver, "//input[@name='distributor[additionalData][fullName]']",
                                               "Ответственный за сделку")
        self.input_email_in_transaction_manager = Input(driver, "//input[@name='distributor[additionalData][email]']",
                                                        "Ответственный за сделку")
        self.input_phone_in_additional_distributor_details = Input(
            driver,
            "//input[@name='distributor[additionalData][phone]']",
            "Телефон. Раздел Дополнительные данные дистрибьютора")
        self.input_name_or_inn_company_chapter_investor_customer = Input(
            driver,
            "//input[@name='customer[companyName]']",
            "Название или ИНН компании. Инвестор/Заказчик")
        self.input_contact_person_chapter_investor_customer = Input(
            driver,
            "//input[@name='customer[fullName]']",
            "Контактное лицо. Инвестор/Заказчик")
        self.input_email_chapter_investor_customer = Input(
            driver,
            "//input[@name='customer[email]']",
            "email. Инвестор/Заказчик")
        self.input_phone_investor_customer = Input(driver, "//input[@name='customer[phone]']",
                                                   "Телефон. Инвестор/Заказчик")
        self.input_name_or_inn_company_designer = Input(driver, "//input[@name='designer[companyName]']",
                                                        "Название или ИНН компании. Раздел Проектировщик")
        self.input_contact_person_chapter_designer = Input(driver, "//input[@name='designer[fullName]']",
                                                           "Контактное лицо. Раздел Проектировщик")
        self.input_email_designer = Input(driver, "//input[@name='designer[email]']", "email. Раздел Проектировщик")
        self.input_phone_designer = Input(driver, "//input[@name='designer[phone]']", "Телефон. Раздел Проектировщик")
        self.input_name_or_inn_company_chapter_general_contractor = Input(
            driver,
            "//input[@name='generalContractor[companyName]']",
            "Название или ИНН компании. Генеральный подрядчик")
        self.input_contact_person_chapter_general_contractor = Input(
            driver,
            "//input[@name='generalContractor[fullName]']",
            "Контактное лицо. Генеральный подрядчик")
        self.input_email_chapter_general_contractor = Input(
            driver,
            "//input[@name='generalContractor[email]']",
            "email. Генеральный подрядчик")
        self.input_phone_general_contractor = Input(driver, "//input[@name='generalContractor[phone]']",
                                                    "Телефон. Раздел Генеральный подрядчик")
        self.input_name_or_inn_company_installer_contractor = Input(driver, "//input[@name='installer[companyName]']",
                                                                    "Название или ИНН компании. Раздел Монтажник/Подрядчик")
        self.input_contact_person_chapter_installer_contractor = Input(driver, "//input[@name='installer[fullName]']",
                                                                       "Контактное лицо. Раздел Монтажник/Подрядчик")
        self.input_email_installer_contractor = Input(driver, "//input[@name='installer[email]']",
                                                      "email. Раздел Монтажник/Подрядчик")
        self.input_phone_installer_contractor = Input(driver, "//input[@name='installer[phone]']",
                                                      "Телефон. Раздел Монтажник/Подрядчик")
        self.input_reason_for_application = Input(driver, "//input[@name='additionalInformation[basis]']",
                                                  "Основание для заявки")
        self.input_message_in_additional_information = Input(driver, "//input[@name='additionalInformation[comment]']",
                                                             "Сообщение. Дополнительная информация")
        self.input_expected_delivery_date = Input(driver, "//input[@name='additionalInformation[purchasePlanDate]']",
                                                  "Ожидаемая дата поставки")

    def click_edit_button(self):
        """Клик по кнопке Редактировать"""
        with allure.step('Клик по кнопке Редактировать заявку'):
            button_edit = self.find_element(CreatingRequestForFasteningLocators.LOCATOR_BUTTON_EDIT)
            self.scroll_to(button_edit)
            self.expecting_clickability(CreatingRequestForFasteningLocators.LOCATOR_BUTTON_EDIT)
            button_edit.click()
            self.waiting_element_is_visibility_located_dom(CreatingRequestForFasteningLocators.LOCATOR_EDIT_HEADER)

    def open_ul_sales_office(self):
        """Раскрытие выпадающего списка Офис продаж в разделе Объект"""
        with allure.step('Раскрытие выпадающего списка Офис продаж в разделе Объект'):
            self.btn_open_closed_ul_sales_office.click()
            self.ul_item_sales_office.wait_visible_on_page()

    def closed_ul_sales_office(self):
        """Закрытие выпадающего списка Офис продаж в разделе Объект"""
        with allure.step('Закрытие выпадающего списка Офис продаж в разделе Объект'):
            self.btn_open_closed_ul_sales_office.click()
            self.ul_item_sales_office.wait_no_visible_on_page()

    def click_investor_customer(self):
        """Клик по разделу Инвестор/заказчик"""
        with allure.step('Клик по разделу Инвестор/заказчик в Заявке'):
            investor_customer = self.find_element(CreatingRequestForFasteningLocators.LOCATOR_BUTTON_INVESTOR_CUSTOMER)
            self.driver.execute_script("arguments[0].click()", investor_customer)
            self.waiting_element_is_visibility_located_dom(
                CreatingRequestForFasteningLocators.LOCATOR_INPUT_COMPANY_NAME_OR_INN)

    def type_email_investor(self, email):
        """Ввод email в поле email в разделе Инвестор/Заказчик"""
        with allure.step(f'Ввод email ({email}) в поле email в разделе Инвестор/Заказчик в Заявке'):
            input_email = self.find_element(CreatingRequestForFasteningLocators.LOCATOR_INPUT_EMAIL_INVESTOR)
            self.driver.execute_script("arguments[0].click()", input_email)
            time.sleep(1)
            input_email.send_keys(Keys.CONTROL + "a")
            input_email.send_keys(email)

    def click_send_for_approval(self):
        """Клик по кнопке Отправить на согласование"""
        with allure.step('Клик по кнопке Отправить на согласование Заявку'):
            button_send = self.find_element(CreatingRequestForFasteningLocators.LOCATOR_BUTTON_SEND_FOR_APPROVAL)
            self.driver.execute_script("arguments[0].click()", button_send)
            self.waiting_for_loader_processing_in_dom(CreatingRequestForFasteningLocators.LOCATOR_LOADER_MODAL)

    def click_learn_more(self):
        """Клик по кнопке Подробнее"""
        with allure.step('Клик по кнопке Подробнее в Заявке'):
            self.is_element_present(*CreatingRequestForFasteningLocators.LOCATOR_BUTTON_LEARN_MORE)
            button_learn_more = self.find_element(CreatingRequestForFasteningLocators.LOCATOR_BUTTON_LEARN_MORE)
            self.driver.execute_script("arguments[0].click()", button_learn_more)
            self.waiting_for_loader_processing_in_dom(FasteningRequestsListLocators.LOCATOR_LOADER_OLD)

    def email_change_check(self, desired_email):
        """Проверка изменения email"""
        with allure.step('Проверка изменения email в Заявке'):
            email_on_the_page = self.find_element(CreatingRequestForFasteningLocators.LOCATOR_INPUT_EMAIL_INVESTOR)
            email_on_the_page = email_on_the_page.get_attribute('value')
            assert desired_email == email_on_the_page, \
                f'{desired_email} новый сгенерированный email не равен email на странице {email_on_the_page}'

    def input_name_object(self, name_object: str):
        """Ввод названия объекта или номера в поле Объект"""
        with allure.step(f'Ввод название объекта или номера ({name_object}) в поле Объект'):
            input_name_obj = self.find_element(CreatingRequestForFasteningLocators.LOCATOR_INPUT_NAME_OBJECT)
            input_name_obj.send_keys(name_object)
            time.sleep(2)
            with allure.step('Ожидание появления выпадающего списка в поле Объект'):
                self.waiting_for_loader_processing_on_page(
                    CreatingRequestForFasteningLocators.LOCATOR_LOADER_IN_INPUT_OBJECT_NAME, sec=90)
                self.waiting_element_is_visibility_on_the_page(
                    CreatingRequestForFasteningLocators.LOCATOR_ACTIVE_UL_OBJECTS,
                    sec=5)

    def select_first_object_in_object_name_field(self):
        """Выбор первого объекта из выпадающего списка в поле ввода объекта"""
        with allure.step('Выбор первого объекта из выпадающего списка в поле ввода объекта'):
            self.expecting_clickability(CreatingRequestForFasteningLocators.LOCATOR_LI_IN_UL_OBJECT_NAME, sec=3)
            item_first_name_object_in_ul = self.find_element(
                CreatingRequestForFasteningLocators.LOCATOR_LI_IN_UL_OBJECT_NAME)
            name_entered_object = item_first_name_object_in_ul.text
            item_first_name_object_in_ul.click()
            self.check_entered_object_in_input_name_object(name_entered_object)

    def check_entered_object_in_input_name_object(self, expected_name_object: str):
        """Проверка выбранного объекта в поле Название объекта"""
        with allure.step('Проверка выбранного объекта в поле Название объекта'):
            name_object = self.find_element(CreatingRequestForFasteningLocators.LOCATOR_INPUT_NAME_OBJECT
                                            ).get_attribute('value')
            assert name_object in expected_name_object, \
                f'Название ожидаемого объекта - ({expected_name_object}) не соответствует выбранному объекту - ' \
                f'({name_object})'

    def checking_selected_sales_office(self, expected_sales_office='Все'):
        """Проверка выбранного офиса продаж"""
        with allure.step(f'Проверка выбранного офиса продаж. Ожидаемый - ({expected_sales_office})'):
            self.selected_sales_office.wait_visible_on_page()
            entered_sales_office = self.selected_sales_office.get_text_element()
            assert entered_sales_office == expected_sales_office, \
                f'Выбранный офис продаж - ({entered_sales_office}) не соответствует ожидаемому - ({expected_sales_office})'

    def check_object_address_field_is_not_editable(self):
        """Проверка, что поле Адрес объекта нередактируемо"""
        with allure.step('Проверка, что поле Адрес объекта нередактируемо'):
            expected_attribute = 'disabled'

            input_address_object = self.input_address_in_object_chapter.find_element()
            attribute_input_address_object = self.get_attributes(input_address_object)
            assert expected_attribute in attribute_input_address_object, \
                f'Поле Адрес объекта редактируемо. Все атрибуты инпута - {attribute_input_address_object}'

    def check_object_address_not_empty(self):
        """Проверка, что поле Адрес объекта не пустое"""
        with allure.step('Проверка, что поле Адрес объекта не пустое'):
            self.waiting_element_is_visibility_located_dom(
                CreatingRequestForFasteningLocators.LOCATOR_INPUT_ADDRESS_OBJECT,
                sec=3)
            input_address_object = self.find_element(CreatingRequestForFasteningLocators.LOCATOR_INPUT_ADDRESS_OBJECT
                                                     ).get_attribute('value')
            assert input_address_object != '', \
                f'Поле Адрес объекта пустое. Значение в поле - ({input_address_object})'

    def open_list_engineering_section(self):
        """Раскрытие выпадающего списка Инженерный раздел"""
        with allure.step('Раскрытие выпадающего списка Инженерный раздел'):
            self.btn_open_closed_ul_engineering_section.click()
            self.active_ul_engineering_section.wait_visible_on_page()

    def closed_list_engineering_section(self):
        """Закрытие выпадающего списка Инженерный раздел"""
        with allure.step('Закрытие выпадающего списка Инженерный раздел'):
            self.btn_open_closed_ul_engineering_section.click()
            self.active_ul_engineering_section.wait_no_presence_in_located_dom()

    def selecting_an_engineering_section(self, engineering_section: str):
        """Выбор инженерного раздела"""
        with allure.step(f'Выбор инженерного раздела {engineering_section}'):
            self.open_list_engineering_section()
            self.expecting_clickability(
                CreatingRequestForFasteningLocators.locator_item_drop_list_by_engineering_section(engineering_section),
                sec=3)
            item_engineering_section = self.find_element(
                CreatingRequestForFasteningLocators.locator_item_drop_list_by_engineering_section(engineering_section))
            item_engineering_section.click()
            selected_engineering_section = self.selected_engineer_section.get_text_element()
            assert selected_engineering_section == engineering_section, \
                f'Выбранный инженерный раздел - ({selected_engineering_section}) не соответствует ожидаемому - ' \
                f'({engineering_section})'

    def open_list_access_to_object_manager(self):
        """Раскрытие выпадающего списка Доступ менеджеру объекта"""
        with allure.step('Раскрытие выпадающего списка Доступ менеджеру объекта'):
            self.btn_open_closed_ul_access_to_object_manager.click()
            self.active_ul_access_to_object_manager.wait_visible_on_page()

    def closed_list_access_to_object_manager(self):
        """Закрытие выпадающего списка Доступ менеджеру объекта"""
        with allure.step('Закрытие выпадающего списка Доступ менеджеру объекта'):
            self.btn_open_closed_ul_access_to_object_manager.click()
            self.active_ul_access_to_object_manager.wait_no_presence_in_located_dom()

    def checking_contents_of_drop_down_list_access_to_object_manager(self):
        """Проверка наполнения выпадающего списка Доступ менеджеру объекта"""
        with allure.step('Проверка наполнения выпадающего списка Доступ менеджеру объекта'):
            expected_item_list = ['Не указано', 'Есть', 'Нет']  # Ожидаемые значения в выпадающем списке
            res_list_error_item = []  # Список со значениями, которые не соответствуют ожидаемым

            item_list_on_page = self.ul_item_access_to_object_manager.get_text_list_element()
            assert len(item_list_on_page) != 0, \
                f'В выпадающем списке Доступ менеджеру объекта не найдено ни одного элемента'

            for el in item_list_on_page:
                if el not in expected_item_list:
                    res_list_error_item.append(el)

            assert len(res_list_error_item) == 0, \
                f'Ожидаемый список - ({expected_item_list}) элементов в выпадающем списке Доступ менеджеру объекта ' \
                f'не соответствует списку на странице - ({item_list_on_page}). Значения на странице, ' \
                f'которые не соответствуют - ({res_list_error_item})'

    def select_value_from_drop_down_list_access_to_object_manager(self, value: str):
        """Выбор значения в выпадающем списке Доступ менеджеру объекта"""
        with allure.step('Выбор значения в выпадающем списке Доступ менеджеру объекта'):
            self.waiting_element_is_visibility_on_the_page(
                CreatingRequestForFasteningLocators.locator_item_in_drop_list_access_to_object_manager(value), sec=3)
            item_in_drop_list = self.find_element(
                CreatingRequestForFasteningLocators.locator_item_in_drop_list_access_to_object_manager(value))
            item_in_drop_list.click()
            selected_item_in_drop_list = self.selected_access_to_object_manager.get_text_element()
            assert selected_item_in_drop_list == value, \
                f'Выбранный доступ менеджеру объекта - ({selected_item_in_drop_list}) не соответствует ожидаемому - ({value})'

    def attaching_specification(self, path_to_file: str):
        """Прикрепление спецификации
        path_to_file - путь к файлу для прикрепления
        """
        with allure.step('Прикрепление спецификации'):
            with allure.step(
                    f'Сохраняем название файла для загрузки в спецификацию из пути к файлу - ({path_to_file})'):
                expected_name_file = path_to_file.split('\\')[-1]

            self.input_specification.filling_input(path_to_file)

            load_file = \
                self.input_with_loaded_specification_files.find_element().get_attribute('value').split('\\')[
                    -1]  # Название подгруженного файла на странице
            assert expected_name_file == load_file, \
                f'В разделе Спецификация не отображается название подгружаемого файла - ({expected_name_file}). ' \
                f'Отображается название - ({load_file})'

    def open_ul_market(self):
        """Раскрытие выпадающего списка рынок"""
        with allure.step('Раскрытие выпадающего списка рынок'):
            self.btn_open_closed_ul_market.click()
            self.ul_item_market.wait_visible_on_page()

    def closed_ul_market(self):
        """Закрытие выпадающего списка рынок"""
        with allure.step('Закрытие выпадающего списка рынок'):
            self.btn_open_closed_ul_market.click()
            self.ul_item_market.wait_no_visible_on_page()

    def check_values_in_market_drop_down_list(self):
        """Проверка значений для выбора в выпадающем списке Рынок"""
        with allure.step('Проверка значений для выбора в выпадающем списке Рынок'):
            expected_value = ['Индустрия', 'Новое строительство', 'Реконструкция']
            values_market_drop = self.ul_item_market.get_text_list_element()
            for el in expected_value:
                assert el in values_market_drop, \
                    f'Ожидаемого значения - ({el}) нет в выпадающем списке Рынок. Все ожидаемые значения - ' \
                    f'({expected_value}). Все значения в выпадающем списке Рынок на странице - ({values_market_drop})'

    def check_selected_market(self, expected_market='Реконструкция'):
        """Проверка выбранного рынка"""
        with allure.step(f'Проверка выбранного рынка. Ожидаемый - ({expected_market})'):
            self.waiting_element_is_visibility_located_dom(CreatingRequestForFasteningLocators.LOCATOR_SELECTED_MARKET,
                                                           sec=5)
            entered_market = self.find_element(CreatingRequestForFasteningLocators.LOCATOR_SELECTED_MARKET
                                               ).text
            assert expected_market == entered_market, \
                f'Выбранный рынок - ({entered_market}) не соответствует ожидаемому - ({expected_market})'

    def click_investor_customer_section_btn(self):
        """Клик по кнопке Инвестор/Заказчик"""
        with allure.step('Клик по кнопке Инвестор/Заказчик'):
            scroll_to_elem = self.find_element(
                CreatingRequestForFasteningLocators.LOCATOR_INVESTOR_CUSTOMER_SECTION_BTN)
            self.scroll_to(scroll_to_elem)

            self.expecting_clickability(CreatingRequestForFasteningLocators.LOCATOR_INVESTOR_CUSTOMER_SECTION_BTN,
                                        sec=3)
            btn_investor_customer_section = self.find_element(
                CreatingRequestForFasteningLocators.LOCATOR_INVESTOR_CUSTOMER_SECTION_BTN)
            btn_investor_customer_section.click()

            time.sleep(0.5)
            open_section_investor_customer = len(self.driver.find_elements(
                *CreatingRequestForFasteningLocators.LOCATOR_INVESTOR_CUSTOMER_SECTION_OPEN))
            assert open_section_investor_customer == 1, \
                f'Раздел Инвестор/Заказчик не раскрыт. len - {open_section_investor_customer}'

    def enter_name_or_inn_in_investor_customer_section(self, inn_or_name_company: str):
        """Ввод названия или ИНН компании в разделе Инвестор/Заказчик"""
        with allure.step(f'Ввод названия или ИНН компании {inn_or_name_company} в разделе Инвестор/Заказчик'):
            self.input_name_or_inn_company_chapter_investor_customer.filling_input(inn_or_name_company)
            self.ul_item_in_name_or_inn_company_investor_customer.scroll_to_elem_action_chains(timeout=5.0)
            self.ul_item_in_name_or_inn_company_investor_customer.click()
            self.check_selected_inn_company_in_investor_customer_section(inn_or_name_company)

    def check_selected_inn_company_in_investor_customer_section(self, expected_inn: str):
        """Проверка ИНН выбранной компании в разделе Инвестор/Заказчик"""
        with allure.step('Проверка ИНН выбранной компании в разделе Инвестор/Заказчик'):
            selected_company = self.find_element(
                CreatingRequestForFasteningLocators.LOCATOR_INPUT_NAME_COMPANY_OR_INN_IN_SECTION_INVESTOR_CUSTOMER
            ).get_attribute('value').split(' ')[0]

            assert expected_inn == selected_company, \
                f'ИНН выбранной компании - ({selected_company}) в разделе Инвестор/Заказчик не соответствует ' \
                f'ожидаемому ИНН - ({expected_inn})'

    def enter_contact_person_in_section_investor_customer(self, name_person: str):
        """Ввод имени контактного лица в разделе Инвестор/Заказчик"""
        with allure.step(f'Ввод имени контактного лица {name_person} в разделе Инвестор/Заказчик'):
            input_contact_person = self.find_element(
                CreatingRequestForFasteningLocators.INPUT_CONTACT_PERSON_INVESTOR_CUSTOMER)
            input_contact_person.send_keys(name_person)

            entering_contact_person = input_contact_person.get_attribute('value')

            assert entering_contact_person == name_person, \
                f'Контактное лицо в поле ввода Контактное лицо - ({entering_contact_person}) не соответствует тому, ' \
                f'которое вводили - ({name_person}) в разделе Инвестор/Заказчик'

    def enter_mail_address_in_section_investor_customer(self, mail_address: str):
        """Ввод мэйла в поле Email в разделе Инвестор/Заказчик"""
        with allure.step(f'Ввод мэйла {mail_address} в поле Email в разделе Инвестор/Заказчик'):
            input_mail = self.find_element(CreatingRequestForFasteningLocators.INPUT_MAIL_ADDRESS_INVESTOR_CUSTOMER)
            input_mail.send_keys(mail_address)

            entering_mail = input_mail.get_attribute('value')
            assert entering_mail == mail_address, \
                f'Мэйл адрес в поле ввода Email - ({entering_mail}) не соответствует тому, который вводили - ' \
                f'({mail_address}) в разделе Инвестор/Заказчик'

    def enter_phone_in_section_investor_customer(self, phone_number: str):
        """Ввод номера телефона в поле Телефон в разделе Инвестор/Заказчик"""
        with allure.step(f'Ввод номера телефона {phone_number} в поле Телефон в разделе Инвестор/Заказчик'):
            phone_number = re.sub(r'[()\-+\s7]', '', phone_number)  # Удаляем символы пробелов, '+', '(', ')', '-'
            print(phone_number)
            input_mail = self.find_element(CreatingRequestForFasteningLocators.INPUT_PHONE_INVESTOR_CUSTOMER)
            input_mail.send_keys(phone_number)

            entering_mail = input_mail.get_attribute('value')
            entering_mail = re.sub(r'[()\-+\s7]', '', entering_mail)  # Удаляем символы пробелов, '+', '(', ')', '-'
            assert entering_mail == phone_number, \
                f'Номер телефона в поле ввода Телефон - ({entering_mail}) не соответствует тому, ' \
                f'который вводили - ({phone_number}) в разделе Инвестор/Заказчик'

    def open_section_general_contractor(self):
        """Раскрытие раздела Генеральный подрядчик"""
        with allure.step('Раскрытие раздела Генеральный подрядчик'):
            self.expecting_clickability(CreatingRequestForFasteningLocators.LOCATOR_GENERAL_CONTRACTOR_BTN, sec=3)
            btn_section_general_contractor = self.find_element(
                CreatingRequestForFasteningLocators.LOCATOR_GENERAL_CONTRACTOR_BTN)
            btn_section_general_contractor.click()
            time.sleep(0.5)
            open_section_general_contractor = len(self.driver.find_elements(
                *CreatingRequestForFasteningLocators.LOCATOR_GENERAL_CONTRACTOR_OPEN))

            assert open_section_general_contractor == 1, \
                f'Раздел Генеральный подрядчик не раскрыт. len - {open_section_general_contractor}'

    def enter_name_or_inn_in_general_contractor_section(self, inn_or_name_company: str):
        """Ввод названия или ИНН компании в разделе Генеральный подрядчик"""
        with allure.step(f'Ввод названия или ИНН компании {inn_or_name_company} в разделе Генеральный подрядчик'):
            self.input_name_or_inn_company_chapter_general_contractor.filling_input(inn_or_name_company)
            self.ul_item_name_or_inn_company_general_contractor.scroll_to_elem_action_chains(timeout=5.0)
            self.ul_item_name_or_inn_company_general_contractor.click()

            self.check_selected_inn_company_in_general_contractor_section(inn_or_name_company)

    def check_selected_inn_company_in_general_contractor_section(self, expected_inn: str):
        """Проверка ИНН выбранной компании в разделе Генеральный подрядчик"""
        with allure.step('Проверка ИНН выбранной компании в разделе Генеральный подрядчик'):
            selected_company = self.find_element(
                CreatingRequestForFasteningLocators.LOCATOR_INPUT_NAME_COMPANY_OR_INN_IN_SECTION_GENERAL_CONTRACTOR
            ).get_attribute('value').split(' ')[0]

            assert expected_inn == selected_company, \
                f'ИНН выбранной компании - ({selected_company}) в разделе Генеральный подрядчик не соответствует ' \
                f'ожидаемому ИНН - ({expected_inn})'

    def enter_contact_person_in_section_general_contractor(self, name_person: str):
        """Ввод имени контактного лица в разделе Генеральный подрядчик"""
        with allure.step(f'Ввод имени контактного лица {name_person} в разделе Генеральный подрядчик'):
            input_contact_person = self.find_element(
                CreatingRequestForFasteningLocators.INPUT_CONTACT_PERSON_SECTION_GENERAL_CONTRACTOR)
            input_contact_person.send_keys(name_person)

            entering_contact_person = input_contact_person.get_attribute('value')
            assert entering_contact_person == name_person, \
                f'Контактное лицо в поле ввода Контактное лицо - ({entering_contact_person}) не соответствует тому, ' \
                f'которое вводили - ({name_person}) в разделе Генеральный подрядчик'

    def enter_mail_address_in_section_general_contractor(self, mail_address: str):
        """Ввод мэйла в поле Email в разделе Генеральный подрядчик"""
        with allure.step(f'Ввод мэйла {mail_address} в поле Email в разделе Генеральный подрядчик'):
            input_mail = self.find_element(CreatingRequestForFasteningLocators.INPUT_MAIL_ADDRESS_GENERAL_CONTRACTOR)
            input_mail.send_keys(mail_address)

            entering_mail = input_mail.get_attribute('value')
            assert entering_mail == mail_address, \
                f'Мэйл адрес в поле ввода Email - ({entering_mail}) не соответствует тому, который вводили - ' \
                f'({mail_address}) в разделе Генеральный подрядчик'

    def enter_phone_in_section_general_contractor(self, phone_number: str):
        """Ввод номера телефона в поле Телефон в разделе Генеральный подрядчик"""
        with allure.step(f'Ввод номера телефона {phone_number} в поле Телефон в разделе Генеральный подрядчик'):
            phone_number = re.sub(r'[()\-+\s7]', '', phone_number)  # Удаляем символы пробелов, '+', '(', ')', '-'

            input_mail = self.find_element(CreatingRequestForFasteningLocators.INPUT_PHONE_GENERAL_CONTRACTOR)
            input_mail.send_keys(phone_number)

            entering_mail = input_mail.get_attribute('value')
            entering_mail = re.sub(r'[()\-+\s7]', '', entering_mail)  # Удаляем символы пробелов, '+', '(', ')', '-'
            assert entering_mail == phone_number, \
                f'Номер телефона в поле ввода Телефон - ({entering_mail}) не соответствует тому, ' \
                f'который вводили - ({phone_number}) в разделе Генеральный подрядчик'

    def activate_toggle_switch_is_buyer_general_contractor(self):
        """Активация тумблера Является закупщиком в разделе Генеральный подрядчик"""
        with allure.step('Активация тумблера Является закупщиком в разделе Генеральный подрядчик'):

            toggle_switch = self.find_element(
                CreatingRequestForFasteningLocators.LOCATOR_TOGGLE_SWITCH_IS_BUYER_GENERAL_CONTRACTOR)
            self.scroll_to_elem_perform(toggle_switch)
            self.expecting_clickability(
                CreatingRequestForFasteningLocators.LOCATOR_TOGGLE_SWITCH_IS_BUYER_GENERAL_CONTRACTOR, sec=3)
            toggle_switch.click()
            is_selected = toggle_switch.is_selected()
            assert is_selected is True, \
                f'Тумблер Является закупщиком в разделе Генеральный подрядчик не выбран. is_selected - {is_selected}'

    def click_btn_send(self):
        """Клик по кнопке Отправить"""
        with allure.step('Клик по кнопке Отправить'):
            btn_send = self.find_element(CreatingRequestForFasteningLocators.LOCATOR_BTN_SEND)
            self.scroll_to_elem_perform(btn_send)
            self.expecting_clickability(CreatingRequestForFasteningLocators.LOCATOR_BTN_SEND, sec=5)
            btn_send.click()
            self.loader_open.waiting_for_loader_no_text_processing_on_page()
            header = len(self.driver.find_elements(*ModalNumberOfYourApplicationLocators.LOCATOR_HEADER))
            assert header == 1, \
                f'Не отображается модалка с номером созданной заявки. len - {header}'


class ModalNumberOfYourApplication(BasePage):
    """Модалка Номер вашей Заявки"""

    def save_num_application(self) -> str:
        """Сохранение номера заявки"""
        with allure.step('Сохранение номера заявки'):
            num_application = self.find_element(ModalNumberOfYourApplicationLocators.LOCATOR_HEADER).text.split(' ')[-1]
            return num_application

    def click_btn_return_to_application_list(self):
        """Клик по кнопке Вернуться в список заявок"""
        with allure.step('Клик по кнопке Вернуться в список заявок'):
            self.expecting_clickability(ModalNumberOfYourApplicationLocators.LOCATOR_BTN_RETURN_TO_APPLICATION_LIST,
                                        sec=3)
            btn_return_to_application_list = self.find_element(
                ModalNumberOfYourApplicationLocators.LOCATOR_BTN_RETURN_TO_APPLICATION_LIST)
            btn_return_to_application_list.click()
            self.waiting_for_loader_processing_on_page(BaseOpenLocators.LOCATOR_SPINNER_NO_TEXT, sec=60)
            header_fastening_request = len(self.driver.find_elements(*FasteningRequestsListLocators.LOCATOR_H1_HEADER))
            assert header_fastening_request == 1, \
                f'Страница Заявки на крепление не открылась. Не найден заголовок Заявки на крепление. ' \
                f'len - {header_fastening_request}'
