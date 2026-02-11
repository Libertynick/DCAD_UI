from datetime import datetime, timedelta

import allure
import pytest

from components.open_components.header_component.nav_bar_ridan import NavBarRidan
from components.open_components.header_component.profile_menu_component import ProfileMenuComponent
from components.open_components.loader_component import LoaderComponent
from config import TestEnvironment
from open_pages.fastening_request.creating_request_for_fastening import CreatingRequestForFasteningPage
from open_pages.main_page.main_page import MainPage
from open_pages.objects_page.fastening_requests_list.fastening_requests_list import FasteningRequestsListPage


@allure.feature('Опеновские тесты')
@allure.story('Заявка на крепление, проверка элементов на странице')
@allure.link('https://rucotfs.ridancorp.net/DanfossDev/CRM/_workitems/edit/51160')
@pytest.mark.stage
def test_51160_application_for_fastening_checking_elements_on_page(browser, authorization_open_fixture):
    """Заявка на крепление, проверка элементов на странице"""
    message_warning_in_participants_of_object = 'Укажите минимум 1 компанию и 1 контактное лицо из списка ниже для отправки анкеты'  # Предупреждение в Участники на объекте
    expected_help_text_in_additional_files = 'Перетащите файл в это поле. Размер файла не более 20 мб.'  # Ожидаемая подсказка в разделе Дополнительные файлы

    link_open_tst = TestEnvironment.LINK_OPEN_TST
    login_open = TestEnvironment.LOGIN_TST_VODOKOMFORT
    password_open = TestEnvironment.PASSWORD_TST_VODOKOMFORT

    # Страницы Опена
    nav_bar_ridan = NavBarRidan(browser)
    profile_menu_component = ProfileMenuComponent(browser)
    page_main = MainPage(browser, link_open_tst)
    page_fastening_request = FasteningRequestsListPage(browser, link_open_tst)
    page_creating_request_for_fastening = CreatingRequestForFasteningPage(browser)
    loader_component = LoaderComponent(browser)

    page_main.open()
    authorization_open_fixture(login_open, password_open)

    name_profile = profile_menu_component.save_name_client()

    nav_bar_ridan.btn_profile.click()
    profile_menu_component.ul_profile_menu.wait_visible_on_page()
    profile_menu_component.btn_objects.click()
    profile_menu_component.btn_fastening_request.click()
    loader_component.waiting_for_loader_no_text_processing_on_page()

    page_fastening_request.click_btn_new_requests()

    # Раздел Объект
    page_creating_request_for_fastening.selected_author_request.should_text_in_element(name_profile)
    page_creating_request_for_fastening.selected_inn_in_chapter_object.check_is_not_empty_element()
    page_creating_request_for_fastening.check_box_enter_name_in_chapter_object.should_check_box_not_selected()
    page_creating_request_for_fastening.ul_item_sales_office.should_elements_alphabetical()
    page_creating_request_for_fastening.open_ul_sales_office()
    page_creating_request_for_fastening.closed_ul_sales_office()
    page_creating_request_for_fastening.checking_selected_sales_office()
    page_creating_request_for_fastening.open_ul_market()
    page_creating_request_for_fastening.closed_ul_market()
    page_creating_request_for_fastening.check_values_in_market_drop_down_list()
    page_creating_request_for_fastening.input_address_in_object_chapter.should_is_not_editable()
    page_creating_request_for_fastening.input_address_in_object_chapter.should_placeholder('Введите значение')
    page_creating_request_for_fastening.open_list_engineering_section()
    page_creating_request_for_fastening.closed_list_engineering_section()
    page_creating_request_for_fastening.selected_engineer_section.should_text_in_element('Выберите из списка')
    page_creating_request_for_fastening.open_list_access_to_object_manager()
    page_creating_request_for_fastening.checking_contents_of_drop_down_list_access_to_object_manager()
    page_creating_request_for_fastening.closed_list_access_to_object_manager()
    page_creating_request_for_fastening.selected_access_to_object_manager.should_text_in_element('Не указано')
    page_creating_request_for_fastening.header_specification.wait_visible_on_page()
    page_creating_request_for_fastening.input_specification.wait_presence_in_located_dom()
    page_creating_request_for_fastening.header_commercial_offer.wait_visible_on_page()
    page_creating_request_for_fastening.input_commercial_offer.wait_presence_in_located_dom()

    # Проверка раздела Дополнительные данные дистрибьютора
    page_creating_request_for_fastening.section_close_additional_distributor_details.wait_presence_in_located_dom()
    page_creating_request_for_fastening.btn_additional_distributor_details.click()
    page_creating_request_for_fastening.section_opened_additional_distributor_details.wait_visible_on_page()

    # page_creating_request_for_fastening.input_transaction_manager.wait_visible_on_page()
    # page_creating_request_for_fastening.input_transaction_manager.should_placeholder('Введите значение')
    page_creating_request_for_fastening.additional_distributor_data_component.filling_person_responsible_for_transaction()

    page_creating_request_for_fastening.input_email_in_transaction_manager.wait_visible_on_page()
    page_creating_request_for_fastening.input_email_in_transaction_manager.should_placeholder('Введите значение')

    page_creating_request_for_fastening.header_country_in_additional_distributor_details.wait_visible_on_page()
    page_creating_request_for_fastening.selected_code_country_in_additional_distributor_details.should_text_in_element(
        '+7')
    page_creating_request_for_fastening.header_phone_in_additional_distributor_details.wait_visible_on_page()
    page_creating_request_for_fastening.input_phone_in_additional_distributor_details.wait_visible_on_page()

    page_creating_request_for_fastening.btn_additional_distributor_details.click()
    page_creating_request_for_fastening.section_close_additional_distributor_details.wait_presence_in_located_dom()

    # Участники на объекте
    page_creating_request_for_fastening.header_participants_of_object.wait_visible_on_page()

    # Инвестор/Заказчик
    page_creating_request_for_fastening.message_warning_in_participants_of_object.should_text_in_element(
        message_warning_in_participants_of_object)
    page_creating_request_for_fastening.btn_open_closed_chapter_investor_customer.scroll_to_elem_action_chains()
    page_creating_request_for_fastening.btn_open_closed_chapter_investor_customer.click()
    page_creating_request_for_fastening.opened_chapter_investor_customer.wait_visible_on_page()

    page_creating_request_for_fastening.input_name_or_inn_company_chapter_investor_customer.wait_visible_on_page()
    page_creating_request_for_fastening.input_name_or_inn_company_chapter_investor_customer.should_placeholder('Ридан')

    page_creating_request_for_fastening.input_contact_person_chapter_investor_customer.wait_visible_on_page()
    page_creating_request_for_fastening.input_contact_person_chapter_investor_customer.should_placeholder(
        'Введите значение')

    page_creating_request_for_fastening.input_email_chapter_investor_customer.wait_visible_on_page()
    page_creating_request_for_fastening.input_email_chapter_investor_customer.should_placeholder('Введите значение')

    page_creating_request_for_fastening.selected_code_country_in_investor_customer.wait_visible_on_page()
    page_creating_request_for_fastening.selected_code_country_in_investor_customer.should_text_in_element('+7')

    page_creating_request_for_fastening.input_phone_investor_customer.wait_visible_on_page()
    # page_creating_request_for_fastening.input_phone_investor_customer.should_placeholder('Введите значение')

    page_creating_request_for_fastening.check_box_enter_name_investor_customer.wait_visible_on_page()
    page_creating_request_for_fastening.check_box_enter_name_investor_customer.should_check_box_not_selected()

    page_creating_request_for_fastening.radio_button_is_purchaser.wait_visible_on_page()
    page_creating_request_for_fastening.radio_button_is_purchaser.radio_button_should_not_selected()

    page_creating_request_for_fastening.btn_open_closed_chapter_investor_customer.click()
    page_creating_request_for_fastening.opened_chapter_investor_customer.wait_no_presence_in_located_dom()

    # Раздел Проектировщик
    page_creating_request_for_fastening.btn_open_closed_chapter_designer.scroll_to_elem_action_chains()
    page_creating_request_for_fastening.btn_open_closed_chapter_designer.click()
    page_creating_request_for_fastening.opened_chapter_designer.wait_visible_on_page()

    page_creating_request_for_fastening.input_name_or_inn_company_designer.wait_visible_on_page()
    page_creating_request_for_fastening.input_name_or_inn_company_designer.should_placeholder('Ридан')

    page_creating_request_for_fastening.input_contact_person_chapter_designer.wait_visible_on_page()
    page_creating_request_for_fastening.input_contact_person_chapter_designer.should_placeholder('Введите значение')

    page_creating_request_for_fastening.input_email_designer.wait_visible_on_page()
    page_creating_request_for_fastening.input_email_designer.should_placeholder('Введите значение')

    page_creating_request_for_fastening.selected_code_country_in_designer.wait_visible_on_page()
    page_creating_request_for_fastening.selected_code_country_in_designer.should_text_in_element('+7')

    page_creating_request_for_fastening.input_phone_designer.wait_visible_on_page()
    # page_creating_request_for_fastening.input_phone_designer.should_placeholder('Введите значение')

    page_creating_request_for_fastening.check_box_enter_name_designer.wait_visible_on_page()
    page_creating_request_for_fastening.check_box_enter_name_designer.should_check_box_not_selected()

    page_creating_request_for_fastening.btn_open_closed_chapter_designer.click()
    page_creating_request_for_fastening.opened_chapter_designer.wait_no_presence_in_located_dom()

    # Раздел Генеральный подрядчик
    page_creating_request_for_fastening.btn_open_closed_chapter_general_contractor.scroll_to_elem_action_chains()
    page_creating_request_for_fastening.btn_open_closed_chapter_general_contractor.click()
    page_creating_request_for_fastening.opened_chapter_general_contractor.wait_visible_on_page()

    page_creating_request_for_fastening.input_name_or_inn_company_chapter_general_contractor.wait_visible_on_page()
    page_creating_request_for_fastening.input_name_or_inn_company_chapter_general_contractor.should_placeholder('Ридан')

    page_creating_request_for_fastening.input_contact_person_chapter_general_contractor.wait_visible_on_page()
    page_creating_request_for_fastening.input_contact_person_chapter_general_contractor.should_placeholder(
        'Введите значение')

    page_creating_request_for_fastening.input_email_chapter_general_contractor.wait_visible_on_page()
    page_creating_request_for_fastening.input_email_chapter_general_contractor.should_placeholder('Введите значение')

    page_creating_request_for_fastening.selected_code_country_in_general_contractor.wait_visible_on_page()
    page_creating_request_for_fastening.selected_code_country_in_general_contractor.should_text_in_element('+7')

    page_creating_request_for_fastening.input_phone_general_contractor.wait_visible_on_page()
    # page_creating_request_for_fastening.input_phone_general_contractor('Введите значение')

    page_creating_request_for_fastening.check_box_enter_name_general_contractor.wait_visible_on_page()
    page_creating_request_for_fastening.check_box_enter_name_general_contractor.should_check_box_not_selected()

    page_creating_request_for_fastening.radio_button_is_general_contractor.wait_visible_on_page()
    page_creating_request_for_fastening.radio_button_is_general_contractor.radio_button_should_not_selected()

    page_creating_request_for_fastening.btn_open_closed_chapter_general_contractor.click()
    page_creating_request_for_fastening.opened_chapter_general_contractor.wait_no_presence_in_located_dom()

    # Раздел Монтажник/Подрядчик
    page_creating_request_for_fastening.btn_open_closed_chapter_installer_contractor.scroll_to_elem_action_chains()
    page_creating_request_for_fastening.btn_open_closed_chapter_installer_contractor.click()
    page_creating_request_for_fastening.opened_chapter_installer_contractor.wait_visible_on_page()

    page_creating_request_for_fastening.input_name_or_inn_company_installer_contractor.wait_visible_on_page()
    page_creating_request_for_fastening.input_name_or_inn_company_installer_contractor.should_placeholder('Ридан')

    page_creating_request_for_fastening.input_contact_person_chapter_installer_contractor.wait_visible_on_page()
    page_creating_request_for_fastening.input_contact_person_chapter_installer_contractor.should_placeholder(
        'Введите значение')

    page_creating_request_for_fastening.input_email_installer_contractor.wait_visible_on_page()
    page_creating_request_for_fastening.input_email_installer_contractor.should_placeholder('Введите значение')

    page_creating_request_for_fastening.selected_code_country_in_installer_contractor.wait_visible_on_page()
    page_creating_request_for_fastening.selected_code_country_in_installer_contractor.should_text_in_element('+7')

    page_creating_request_for_fastening.input_phone_installer_contractor.wait_visible_on_page()
    # page_creating_request_for_fastening.input_phone_installer_contractor.should_placeholder('Введите значение')

    page_creating_request_for_fastening.check_box_enter_name_installer_contractor.wait_visible_on_page()
    page_creating_request_for_fastening.check_box_enter_name_installer_contractor.should_check_box_not_selected()

    page_creating_request_for_fastening.radio_button_is_installer_contractor.wait_visible_on_page()
    page_creating_request_for_fastening.radio_button_is_installer_contractor.radio_button_should_not_selected()

    page_creating_request_for_fastening.btn_open_closed_chapter_installer_contractor.click()
    page_creating_request_for_fastening.opened_chapter_installer_contractor.wait_no_presence_in_located_dom()

    # Раздел Дополнительная информация
    page_creating_request_for_fastening.header_additional_information.wait_visible_on_page()
    page_creating_request_for_fastening.header_reason_for_application.wait_visible_on_page()

    page_creating_request_for_fastening.input_reason_for_application.wait_visible_on_page()
    page_creating_request_for_fastening.input_reason_for_application.should_placeholder('Введите значение')

    page_creating_request_for_fastening.input_message_in_additional_information.wait_visible_on_page()
    page_creating_request_for_fastening.input_message_in_additional_information.should_placeholder('Введите значение')

    page_creating_request_for_fastening.input_expected_delivery_date.wait_visible_on_page()
    page_creating_request_for_fastening.input_expected_delivery_date.should_value_in_input_field('')

    page_creating_request_for_fastening.btn_calendar_in_expected_delivery_date.wait_visible_on_page()

    # Получаем сегодняшнюю дату
    today = datetime.today()
    # Вычисляем вчерашнюю дату
    yesterday = (today - timedelta(days=1)).strftime('%d.%m.%Y')
    page_creating_request_for_fastening.input_expected_delivery_date.filling_input(yesterday)
    page_creating_request_for_fastening.input_message_in_additional_information.click()
    page_creating_request_for_fastening.input_expected_delivery_date.should_value_in_input_field('')

    # Раздел Дополнительные файлы
    page_creating_request_for_fastening.header_additional_files.wait_visible_on_page()
    page_creating_request_for_fastening.help_text_in_additional_files.wait_visible_on_page()
    page_creating_request_for_fastening.help_text_in_additional_files.should_text_in_element(
        expected_help_text_in_additional_files)

    page_creating_request_for_fastening.btn_back.wait_visible_on_page()
    page_creating_request_for_fastening.btn_back.check_enabled()

    page_creating_request_for_fastening.btn_save_as_draft.wait_visible_on_page()
    page_creating_request_for_fastening.btn_save_as_draft.check_enabled()

    page_creating_request_for_fastening.btn_send.wait_visible_on_page()
    page_creating_request_for_fastening.btn_send.check_enabled()
