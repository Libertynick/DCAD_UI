import time

import allure
from selenium.webdriver.chrome.webdriver import WebDriver

from base_page.base_page import BasePage
from base_page.base_page_locators import BaseOpenLocators
from components.open_components.loader_component import LoaderComponent
from elements.button import Button
from open_pages.fastening_request.creating_request_for_fastening import CreatingRequestForFasteningPage
from open_pages.fastening_request.fastening_request_locators import FasteningRequestLocators
from open_pages.objects_page.fastening_requests_list.locators_fastening_requests_list import \
    FasteningRequestsListLocators


@allure.feature('Страница Заявки на крепление')
class FasteningRequestsListPage(BasePage):
    """Страница Заявки на крепление (список заявок)"""

    def __init__(self, driver: WebDriver, url=''):
        super().__init__(driver, url)

        self.loader_component = LoaderComponent(driver)
        self.creating_request_for_fastening_page = CreatingRequestForFasteningPage(driver)

        # Кнопки
        self.btn_create_request = Button(
            driver,
            "//a[@href='/cabinet/objects/applications-for-attachment/create']",
            "+ Создать заявку")

    def click_btn_new_requests(self):
        """Клик по кнопке + Создать новую заявку"""
        with allure.step('Клик по кнопке + Создать новую заявку'):
            self.btn_create_request.wait_visible_on_page(timeout=15)
            self.btn_create_request.click()
            self.loader_component.waiting_for_loader_no_text_processing_on_page()
            self.creating_request_for_fastening_page.header.wait_visible_on_page(timeout=30)

    def click_advanced_search(self):
        """Клик по кнопке Расширенный поиск"""
        with allure.step('Клик по кнопке Расширенный поиск'):
            advanced_search = self.find_element(FasteningRequestsListLocators.LOCATOR_ADVANCED_SEARCH)
            advanced_search.click()
            time.sleep(0.5)
            open_block_advanced_search = len(self.driver.find_elements(
                *FasteningRequestsListLocators.LOCATOR_BLOCK_OPEN_ADVANCED_SEARCH))
            assert open_block_advanced_search == 1, \
                f'Блок расширенного поиска не открылся. len - {open_block_advanced_search}'

    def search_fastening_requests(self, application_number):
        """Поиск заявки на крепление по номеру и в статусе Принята"""
        with allure.step(f'Поиск заявки на крепление {application_number} по номеру и в статусе Принята'):
            with allure.step('Поиск заявки на крепление по номеру, ввод номера'):
                input_search_advanced = self.find_element(FasteningRequestsListLocators.LOCATOR_INPUT_NAME_OBJECT)
                input_search_advanced.send_keys(application_number)
                with allure.step('Клик на кнопку Найти'):
                    button_search = self.find_element(FasteningRequestsListLocators.LOCATOR_BUTTON_SEARCH)
                    button_search.click()
                    self.loader_open.waiting_for_loader_no_text_processing_on_page()
                    application = self.driver.find_elements(*FasteningRequestsListLocators.LOCATOR_LINK_APPLICATION)
                    application_count = len(application)
                    assert application_count == 1, \
                        f'В результате поиска найдено больше одной заявки. len - {application_count}'
                    num_application = application[0].text
                    assert num_application == application_number, \
                        f'В результате поиска найдена не та заявка - ({num_application}). Искомая - ({application_number})'

    def go_to_fastening_requests(self, application_number):
        """Переход в Заявку на крепление"""
        with allure.step(f'Клик на найденную заявку {application_number}'):
            fastening_requests = self.find_element(
                FasteningRequestsListLocators.locator_btn_fastening_request(application_number))
            fastening_requests.click()
            self.waiting_for_loader_processing_on_page(BaseOpenLocators.LOCATOR_SPINNER_NO_TEXT)
            self.waiting_element_is_visibility_on_the_page(FasteningRequestLocators.locator_header(application_number),
                                                           sec=5)
