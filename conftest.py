from typing import List

import allure
import pytest
from selenium.common import NoAlertPresentException
from selenium.webdriver.chrome.webdriver import WebDriver

from base_page.base_page import BasePage

from components.dcad_components.authorization_dcad_page import AuthorizationDcadPage
from components.dcad_components.header_dcad_component import HeaderDcadComponent
from components.open_components.authorization_modal import AuthorizationModal
from components.open_components.cookie_component import CookieComponentModal
from components.open_components.header_component.nav_bar_ridan import NavBarRidan
from config import TestEnvironment
from crm_pages.athorization_page.authorization_page import AuthorizationPage
from crm_pages.header_page.header_page import HeaderComponent
from crm_pages.pq_page.pq_page import PqPage
from crm_pages.pq_page.pq_page_locators import PqPageLocators
from tools import helper


@pytest.fixture
def authorization_open_fixture(browser: WebDriver):
    def _authorization_open(login: str, password: str):
        """
        Авторизация в Опен
        :param login: Логин
        :param password: Пароль
        """
        nav_bar_ridan = NavBarRidan(browser)
        authorization_modal = AuthorizationModal(browser)
        cookie_component = CookieComponentModal(browser)

        nav_bar_ridan.btn_to_come_in.click()
        authorization_modal.should_header_visible()
        authorization_modal.filling_email(login)
        authorization_modal.filling_password(password)
        authorization_modal.click_btn_come_in()

        cookie_component.click_btn_i_see_cookie()

    return _authorization_open


@pytest.fixture
def authorization_dcad_fixture(browser: WebDriver):
    def _authorization_dcad(login: str, password: str):
        """
        Авторизация в DCAD
        :param login: Email для входа
        :param password: Пароль
        """
        header_dcad = HeaderDcadComponent(browser)
        authorization_page = AuthorizationDcadPage(browser)

        # Проверяем, не авторизован ли уже пользователь
        if header_dcad.is_user_logged_in():
            print(f'Пользователь уже авторизован')
            return

        # Проверяем что форма авторизации открылась
        authorization_page.should_header_visible()

        # Заполняем форму
        authorization_page.filling_email(login)
        authorization_page.filling_password(password)

        # Отправляем форму
        authorization_page.click_btn_submit()
        header_dcad.wait_user_logged_in()

    return _authorization_dcad


@pytest.fixture
def emergence_of_different_types_of_agreements_in_kp(browser):
    def _emergence_of_different_types_of_agreements(
            id_pq: str,
            num_pq: str,
            type_of_agreement_visible_after_save: list,
            type_of_agreement_visible_after_save_after_change_condition: list,
            delivery_type: str,
            expected_status_agreement: dict
    ):
        """
        Действия по проверке возникновения согласований в разных видах КП.
        С бесплатной доставкой на адрес, условия оплаты - согласование условий оплаты
        :param id_pq: id КП
        :param num_pq: номер КП
        :param type_of_agreement_visible_after_save: Ожидаемые типы согласований после сохранения
        :param type_of_agreement_visible_after_save_after_change_condition:  Ожидаемые типы согласований после изменений условий в КП
        :param delivery_type: Вид доставки (Доставка на указанный адрес, стандартные договорные условия)
        :param expected_status_agreement: Ожидаемые статусы у согласований
        :return: Функция, в которой действия по проверке возникновения типов согласований в разных видах КП
        """

        link_pq = TestEnvironment.LINK_PQ_IN_CRM
        link_pq_total = link_pq + id_pq
        page_pq = PqPage(browser, link_pq_total)
        # Открываем КП в срм
        page_pq.open()
        page_pq.click_btn_save_pq()
        page_pq.check_visible_type_of_agreement(type_of_agreement_visible_after_save, num_pq)
        page_pq.switching_currency_to_a_fixed_rate()
        page_pq.selection_of_delivery_conditions(delivery_type)
        page_pq.choice_of_free_payment_mode()
        page_pq.expanding_payment_terms_menu()
        page_pq.click_on_button_agree_on_payment_terms()
        page_pq.click_btn_save_pq()
        page_pq.check_visible_type_of_agreement(type_of_agreement_visible_after_save_after_change_condition, num_pq)
        page_pq.send_for_approval_pq_page()
        page_pq.status_of_checkpoint_must_be_approval()

    return _emergence_of_different_types_of_agreements


@pytest.fixture
def auth_crm_extru_start(browser):
    def _auth_start(ruco='RUCO1681', password='1234'):
        """
            Авторизация в срм при старте теста.
            По умолчанию используется пользователь:
            - ruco: RUCO1681 (Оганесян Левон)
            - Пароль: 1234
            :param ruco: ruco пользователя (логин)
            :param password: Пароль
            :return: _auth_start - функция, выполняющая авторизацию в срм
        """
        with allure.step(f'Авторизация в срм. Логин - {ruco}, пароль - {password}'):
            link_auth = TestEnvironment.LINK_CRM_TST_AUTHORIZATION
            page_auth = AuthorizationPage(browser, link_auth)

            page_auth.open()
            page_auth.authorization_extru(login=ruco, password=password)

    return _auth_start


@pytest.fixture
def auth_extru_crm_from_authorized_page(browser):
    """Авторизация в экстру срм с уже авторизованной страницы"""

    def _auth_extru(url_page: str, name_user='RUCO1681', password='1234'):
        """
        Авторизация в экстру срм с уже авторизованной страницы
        :param url_page:  url страницы, с которой будет авторизация
        :param name_user: Имя пользователя. Для дальнейшего определения ruco
        :return: Функция, которая проходит авторизацию в срм со страницы срм
        """
        with allure.step(
                f'Авторизация в экстру срм с уже авторизованной страницы {url_page}. Пользователь - {name_user}'):
            page_pq = PqPage(browser, url=url_page)
            page_header = HeaderComponent(browser)
            page_auth = AuthorizationPage(browser, TestEnvironment.LINK_CRM_TST_AUTHORIZATION)

            cookie_session = page_pq.get_cookie_session()
            ruco = helper.get_ruco_user_crm_by_name(cookie=cookie_session, name_user=name_user)
            print(ruco)
            helper.release_all_substitutions_crm(cookie_session)
            page_header.activate_profile_menu()
            page_header.btn_logout.click()

            page_auth.open()
            page_auth.authorization_extru(login=ruco, password=password)

            page_pq.open()

    return _auth_extru


@pytest.fixture
def agreement_on_all_conditions_extru(browser, auth_extru_crm_from_authorized_page):
    """Согласование всех условий на внешнем сайте extru"""

    def _agreement_all():
        with allure.step('Согласование всех условий на внешнем сайте extru'):
            link_pq = browser.current_url
            page_base = BasePage(browser, link_pq)

            page_base.waiting_element_is_visibility_located_dom(PqPageLocators.LOCATOR_CONSOLIDATION_CHECKBOX, sec=30)
            count_consolidation_checkbox = browser.find_elements(
                *PqPageLocators.LOCATOR_CONSOLIDATION_CHECKBOX)  # количество согласований
            while len(count_consolidation_checkbox) != 0:

                pq_page = PqPage(browser, url=link_pq)

                count_warning = browser.find_elements(*PqPageLocators.LOCATOR_ORANGE_AGREEMENT_FLAGS
                                                      )  # Согласователи с оранжевой меткой
                if len(count_warning) != 0:
                    conciliator_list = pq_page.agreement_with_orange_mark()

                else:
                    conciliator_list = pq_page.agreement_with_blue_mark()

                print(conciliator_list)

                auth_extru_crm_from_authorized_page(link_pq, conciliator_list[0])
                pq_page.reconciliation_of_outdated_costs()
                with allure.step('Клик по галочке согласование напротив согласователя'):
                    page_base.waiting_element_is_visibility_located_dom(PqPageLocators.LOCATOR_AGREEMENT_TRUE, sec=15)
                    agreement_true = page_base.find_element(PqPageLocators.LOCATOR_AGREEMENT_TRUE)
                    page_base.scroll_to(agreement_true)
                    page_base.expecting_clickability(PqPageLocators.LOCATOR_AGREEMENT_TRUE, sec=10)

                    agreement_true = page_base.find_element(PqPageLocators.LOCATOR_AGREEMENT_TRUE)
                    agreement_true.click()
                    page_base.waiting_element_is_visibility_located_dom(PqPageLocators.LOCATOR_H4_AGREEMENT, sec=90)

                pq_page.agreement_kp_for_client()
                pq_page.entering_a_comment_for_approval()
                pq_page.click_on_the_agree_button()

                count_consolidation_checkbox = browser.find_elements(
                    *PqPageLocators.LOCATOR_CONSOLIDATION_CHECKBOX)  # количество согласований

    return _agreement_all


@pytest.fixture
def get_article_from_parametrize_test(request: pytest.FixtureRequest) -> List[str]:
    """Получение артикулов из параметризации(параметр - article)"""
    article_for_test = request.node.funcargs.get('article')
    article_for_test = ' '.join(article_for_test).split()[::2]
    return article_for_test
