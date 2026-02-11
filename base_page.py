import datetime
import os
from pathlib import Path

from faker import Faker
from requests.auth import HTTPBasicAuth
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from base_page.base_page_locators import BaseCrmLocators, BaseOpenLocators
from components.crm_components.loader_component_crm import LoaderComponentsCrm
from components.dcad_components.loader_dcad_component import LoaderDcadComponent
from components.open_components.loader_component import LoaderComponent

from crm_pages.header_page.header_page_locators import ToolsLocators
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import allure

from tools.validators import assertions


class BasePage:

    def __init__(self, driver, url: str = None):
        self.driver: WebDriver = driver
        self.url = url

        self.loader_crm = LoaderComponentsCrm(driver)
        self.loader_open = LoaderComponent(driver)
        self.loader_dcad = LoaderDcadComponent(driver)

    def open(self):
        # try:
        #     self.driver.get(self.url)
        #     size_window = self.driver.get_window_size()
        #     print(size_window, 'size_window')
        #
        # except MyTimeoutException as ex:
        #     print(ex.msg)
        #     self.driver.refresh()
        with allure.step(f'Открытие страницы {self.url}'):
            self.driver.get(self.url)
            time.sleep(1)

            self.loader_crm.waiting_loader_processing_on_page()
            self.loader_open.waiting_for_loader_no_text_processing_on_page()

    def find_element(self, locator, sec=10):
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
        with allure.step('Поиск одного элемента'):
            return WebDriverWait(driver=self.driver, timeout=sec, ignored_exceptions=ignored_exceptions
                                 ).until(EC.presence_of_element_located(locator),
                                         message=f"Can't find element by locator {locator}")

    def find_elements(self, locator, sec=10):
        with allure.step('Поиск нескольких элементов с одним локатором'):
            return WebDriverWait(self.driver, sec).until(EC.presence_of_all_elements_located(locator),
                                                         message=f"Can't find elements by locator {locator}")

    def waiting_for_loader_processing_on_page(self, locator, sec=180):
        """Ожидание отработки лоадера. Ожидает невидимость на странице"""
        with allure.step(f'Ожидание отработки лоадера. Ожидает невидимость на странице. sec={sec}'):
            wait = WebDriverWait(self.driver, sec)
            return wait.until(EC.invisibility_of_element(self.find_element(locator)),
                              message='Ошибка ожидания прелоадера')

    def waiting_for_loader_processing_in_dom(self, locator, sec=60):
        """Ожидание отработки лоадера. Ожидает невидимость в DOM дереве"""
        with allure.step(f'Ожидание отработки лоадера. Ожидает невидимость в DOM дереве. sec={sec}'):
            wait = WebDriverWait(self.driver, sec)
            wait.until(EC.invisibility_of_element_located(locator))

    def is_element_present(self, how, what):
        with allure.step('Ожидание отображения на странице элемента'):
            try:
                self.driver.find_element(how, what)
            except NoSuchElementException:
                return False
            return True

    def waiting_element_is_visibility_on_the_page(self, locator, sec=10):
        """Ожидание появления элемента на странице"""
        with allure.step(f'Ожидание появления элемента на странице. sec={sec}'):
            wait = WebDriverWait(self.driver, timeout=sec)
            return wait.until(EC.visibility_of(self.find_element(locator, sec=sec)),
                              message=f'{locator} Элемент не виден на странице')

    def waiting_element_is_visibility_located_dom(self, locator, sec=20):
        """Ожидание видимости элемента в DOM дереве"""
        with allure.step(f'Ожидание видимости элемента в DOM дереве. Время ожидания в сек - {sec}'):
            wait = WebDriverWait(self.driver, timeout=sec)
            return wait.until(EC.presence_of_element_located(locator),
                              message=f'{locator} Элемент не присутствует в DOM- дереве')

    def waiting_element_invisibility(self, locator, sec=20):
        """Ожидание невидимости элемента на странице"""
        with allure.step(f'Ожидание невидимости элемента на странице. sec={sec}'):
            wait = WebDriverWait(self.driver, sec)
            return wait.until(EC.invisibility_of_element(locator),
                              message=f'{locator} Элемент виден на странице')

    def expecting_clickability(self, locator, sec=20):
        """Ожидание кликабельности элемента"""
        with allure.step(f'Ожидание кликабельности элемента. sec={sec}'):
            wait = WebDriverWait(self.driver, sec)
            return wait.until(EC.element_to_be_clickable(self.find_element(locator, sec=sec)),
                              message=f'Элемент {locator} не кликабелен')

    def scroll_to(self, elem):
        with allure.step('Прокрутка страницы до элемента'):
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
            time.sleep(1)

    def scroll_to_height(self):
        with allure.step('Прокрутка страницы до самого верха'):
            self.driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")

    def scroll_to_elem_perform(self, elem):
        with allure.step('Прокрутка страницы до элемента'):
            actions = ActionChains(self.driver)
            actions.move_to_element(elem).perform()
            time.sleep(2)

    def switching_window_by_num_window(self, num_window: int):
        """Переход на вкладку
        num_window - номер окна для переключения"""
        with allure.step('Переход на вкладку'):
            window_after = self.driver.window_handles[num_window]
            self.driver.switch_to.window(window_after)

    def switching_window_by_id_window(self, id_window: str):
        """
        Переключение на вкладку по id вкладки
        :param id_window: id вкладки
        """
        with allure.step(f'Переключение на вкладку по id вкладки'):
            self.driver.switch_to.window(id_window)

    def screen_shot(self):
        with allure.step('Скриншот страницы'):
            now_data = datetime.datetime.utcnow().strftime("%Y.%m.%d.%H.%M.%S")
            name_screenshot = 'screenshot' + now_data + '.png'
            self.driver.save_screenshot("C:\\RIDAN\\autotests\\open_project\\screen\\" + name_screenshot)

    @staticmethod
    def link_not_fall(links: list):
        """Проверка открытия ссылок"""
        with allure.step('Проверка открытия ссылок'):
            result = []

            for link in links:
                r = requests.get(link, verify=False)
                status_code = r.status_code
                try:
                    print(status_code)
                    assert status_code == 200
                except AssertionError:
                    print(f'{status_code} != 200, {link}')
                    result.append(f'Status code - {status_code},  Ссылка - {link}')
            return result

    def switch_to_frame(self, locator_frame):
        """Переключение во фрэйм. Locator_frame- локатор фрэйма"""
        with allure.step('Переключение во фрэйм'):
            iframe = self.find_element(locator_frame)
            self.driver.switch_to.frame(iframe)

    @staticmethod
    def checking_the_download_document_in_the_download_folder(name_file: str, time_load: int = 30):
        """Проверка скачивания документа в папке загрузки,
        :param name_file - имя документа
        :param time_load: Ожидаемое время скачивания"""
        with allure.step(f'Проверка скачивания документа ({name_file}) в папке загрузки'):
            downloads_path = str(Path.home() / "Downloads")
            waiting_time = 3  # секунды
            res_search = False

            time.sleep(waiting_time)
            while time_load != 0:
                time.sleep(waiting_time)
                for address, dirs, files in os.walk(downloads_path):
                    for file in files:
                        if file == name_file:
                            print(file, os.path.join(address, file))
                            res_search = True
                time_load -= waiting_time
                if res_search:
                    time_load = 0
            print(res_search, 'res_search')
            assert res_search is True, f'Документ - ({name_file}) не найден по пути - {downloads_path}. Время ожидания- {time_load} сек.'

    @staticmethod
    def search_for_the_last_downloaded_file_in_a_folder(folder_path: str) -> str:
        """Поиск последнего загруженного файла в папке
        folder_path - путь к папке
        """
        with allure.step(f'Поиск последнего загруженного файла в папке {folder_path}'):
            files = os.listdir(folder_path)
            last_file = ''
            if files:
                files = [os.path.join(folder_path, file) for file in files]
                files = [file for file in files if os.path.isfile(file)]
                latest_file_path = max(files, key=os.path.getctime)
                last_file = latest_file_path.split('\\')[-1]
            return last_file

    @staticmethod
    def delete_file_by_name_in_download_folder(file_name: str):
        """Удаление файла по имени в папке Загрузки"""
        with allure.step(f'Удаление файла {file_name} по имени в папке Загрузки'):
            downloads_path = str(Path.home() / "Downloads")
            try:
                delete_file = os.path.join(downloads_path, file_name)
                os.remove(delete_file)
            except FileNotFoundError:
                print(f'Файл {file_name} не найден в папке {downloads_path} для удаления')

    def ctrl_click_link(self, element):
        """Ctrl+ click по ссылке, открытие в новой вкладке"""
        with allure.step('Ctrl+ click по ссылке, открытие в новой вкладке'):
            actions = ActionChains(self.driver)
            actions. \
                key_down(Keys.CONTROL) \
                .click(element) \
                .key_up(Keys.CONTROL) \
                .perform()

    def click_js(self, element):
        """Клик через javaScript"""
        with allure.step('Клик через javaScript'):
            self.driver.execute_script("arguments[0].click()", element)

    def get_attributes(self, element) -> dict:
        with allure.step('Получение всех атрибутов у элемента'):
            return self.driver.execute_script(
                """
                let attr = arguments[0].attributes;
                let items = {}; 
                for (let i = 0; i < attr.length; i++) {
                    items[attr[i].name] = attr[i].value;
                }
                return items;
                """,
                element
            )

    @staticmethod
    def generation_mail_address() -> str:
        """Генерация мэйл адреса"""
        with allure.step('Генерация мэйл адреса'):
            fake = Faker('ru_RU')
            return fake.email(domain='mail.ru')

    @staticmethod
    def generation_phone() -> str:
        with allure.step('Генерация номера телефона'):
            fake = Faker('ru_RU')
            return fake.phone_number()

    @staticmethod
    def generation_name_surname_patronymic() -> str:
        """Генерация имени, фамилии, отчества"""
        with allure.step('Генерация фамилии, отчества'):
            fake = Faker('ru_RU')
            return fake.name()

    def get_cookie_session(self) -> dict:
        """Получение все Куки"""
        with allure.step('Получение все Куки'):
            all_cookies = self.driver.get_cookies()
            cookies_dict = {}
            for cookie in all_cookies:
                # if cookie['name'] == 'ridan_session':
                cookies_dict[cookie['name']] = cookie['value']
            return cookies_dict

    @staticmethod
    def captcha_solution_in_tst(all_cookies: dict) -> list:
        """Решение капчи"""
        with allure.step('Решение капчи'):
            url = 'http://ruecom-open-tst1.ridancorp.net/'
            user = 'py-tests'
            password = 'VwMAvpMwTz7FL2dfHXraqYqDZciNNwNAMLD28396GwU2ia48qdodEuvGmtTv4i6n'
            api = 'api/v1/captcha/answer'
            answer_and_cookie = []
            basic = HTTPBasicAuth(user, password)

            # Получение сессии по кукам
            sess = requests.Session()
            response = sess.get(f'{url}{api}', auth=basic, cookies=all_cookies)

            # print('---------')
            # print(response, response.status_code, 'response')
            # with open("res.txt", "w") as file:
            #     file.write(response.text)
            # print('---------')

            # достаем решение капчи
            response_json = response.json()
            # print(response_json, 'response_json')
            response_answer = response_json['data']['answer']

            # берем куки капчи в момент обращения к решению
            cookie_captcha = sess.get('http://ruecom-open-tst1.ridancorp.net/sanctum/csrf-cookie', cookies=all_cookies)

            answer_and_cookie.append(response_answer)
            answer_and_cookie.append(cookie_captcha.cookies.get_dict())
            return answer_and_cookie

    def get_text_without_nesting(self, element: WebElement) -> str:
        """
        Получить текст без текста вложенных элементов
        :param element: web element
        :return: Текст веб элемента без вложенных в него элементов
        """
        with allure.step('Получить текст без текста вложенных элементов'):
            text = self.driver.execute_script("""
                let textContent = '';
                for (let node of arguments[0].childNodes) {
                    if (node.nodeType === Node.TEXT_NODE && node.textContent.trim() !== '') {
                        textContent = node.textContent.trim();
                        break;
                    }
                }
                return textContent;
            """, element)
            return text

    def open_url_new_window(self, url: str):
        """
        Открыть страницу в новой вкладке
        :param url: Адрес страницы
        """
        with allure.step(f'Открытие {url} в новой вкладке'):
            self.driver.execute_script("window.open(arguments[0])", url)
            self.switching_window_by_num_window(-1)
            self.loader_crm.waiting_loader_processing_on_page()
            self.loader_open.waiting_for_loader_no_text_processing_on_page()

    def save_current_window(self) -> str:
        """Сохранение текущей вкладки"""
        with allure.step(f'Сохранение текущей вкладки'):
            current_window = self.driver.current_window_handle
            return current_window

    def get_current_url(self) -> str:
        """Получение текущего url"""
        with allure.step('Получение текущего url'):
            WebDriverWait(self.driver, timeout=5).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            return self.driver.current_url

    def check_url_page(self, expected_url: str) -> None:
        """
        Проверка url страницы
        :param expected_url: Ожидаемый url страницы
        """
        with allure.step(f'Проверка, что url страницы- {expected_url}'):
            current_url = self.get_current_url()
            assertions.assert_eq(
                actual_value=current_url,
                expected_value=expected_url,
                allure_title='Сверяем url текущий с ожидаемым',
                error_message=f'URL страницы не соответствует ожидаемому. '
                              f'Страницы- {current_url}; ожидаемый- {expected_url}'
            )

    def reload_page_open_or_crm(self):
        """Перезагрузка страницы Опен или СРМ"""
        self.driver.refresh()
        self.loader_crm.waiting_loader_processing_on_page()
        self.loader_open.waiting_for_loader_no_text_processing_on_page()

    def history_back(self) -> None:
        """На предыдущую страницу"""
        with allure.step('Возврат на предыдущую страницу'):
            self.driver.execute_script('window.history.back();')
            self.loader_open.waiting_for_loader_no_text_processing_on_page()
            self.loader_crm.waiting_loader_processing_on_page()

    def action_chains_esc(self) -> None:
        """Нажатие ESC на клавиатуре"""
        with allure.step('Нажатие ESC на клавиатуре'):
            self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)


class BasePageCrm(BasePage):

    def __int__(self):
        super().__init__(self.driver, self.url)

    def waiting_present_element(self, locator, sec=90):
        """Ожидание появления элемента на странице"""
        with allure.step(f'Ожидание появления элемента на странице. sec={sec}'):
            wait = WebDriverWait(self.driver, sec)
            wait.until(EC.presence_of_element_located(locator), message=f'Ошибка ожидания элемента {locator}')

    def authentication_crm(self, url_address, login, password):
        """Аутентификация в crm"""
        with allure.step(f'Аутентификация в crm. logi - {login}; password - {password}'):
            url_address = url_address.split('//')[1]
            url = f'http://{login}:{password}@{url_address}'
            page = BasePage(self.driver, url)
            page.open()
            time.sleep(2)
        # basic = HTTPBasicAuth(login, password)
        # response = requests.get(url_address, auth=basic)
        # print(response)

    def click_button_testing_tools(self):
        """Клик по кнопке Инструменты тестирования"""
        with allure.step('Клик по кнопке Инструменты тестирования'):
            self.scroll_to_height()
            self.expecting_clickability(BaseCrmLocators.LOCATOR_BUTTON_TESTING_TOOLS)
            button_testing_tools = self.find_element(BaseCrmLocators.LOCATOR_BUTTON_TESTING_TOOLS)
            button_testing_tools.click()
            with allure.step('Проверка, что появился заголовок Инструменты тестирования'):
                self.waiting_element_is_visibility_located_dom(BaseCrmLocators.LOCATOR_H4_TESTING_TOOLS)

    def click_button_change_for_yourself(self):
        """Клик по кнопке Смена на себя в инструментах тестирования"""
        with allure.step('Клик по кнопке Смена на себя в инструментах тестирования'):
            button_yourself_list = self.driver.find_elements(*BaseCrmLocators.LOCATOR_BUTTON_CHANGE_FOR_YOURSELF)
            if len(button_yourself_list) > 0:
                self.expecting_clickability(BaseCrmLocators.LOCATOR_BUTTON_CHANGE_FOR_YOURSELF)
                self.find_element(BaseCrmLocators.LOCATOR_BUTTON_CHANGE_FOR_YOURSELF).click()
                time.sleep(2)
                with allure.step('Ожидание отработки лоадера'):
                    self.waiting_element_invisibility(BaseCrmLocators.LOCATOR_BUTTON_CHANGE_FOR_YOURSELF)
                    self.waiting_for_loader_processing_in_dom(BaseCrmLocators.LOCATOR_LOADER)
                    self.waiting_element_is_visibility_located_dom(BaseCrmLocators.LOCATOR_BODY)
                    self.waiting_for_loader_processing_in_dom(BaseCrmLocators.LOCATOR_LOADER)
                self.click_button_testing_tools()

    def click_button_release_all_substitutions(self):
        """Клик по кнопке Освободить все подмены"""
        with allure.step('Клик по кнопке Освободить все подмены'):
            self.expecting_clickability(BaseCrmLocators.LOCATOR_BTN_RELEASE_ALL_SUBSTITUTIONS, sec=5)
            btn_release_all_substitutions = self.find_element(BaseCrmLocators.LOCATOR_BTN_RELEASE_ALL_SUBSTITUTIONS)
            self.click_js(btn_release_all_substitutions)
            with allure.step('Ожидание отработки лоадера'):
                self.waiting_for_loader_processing_in_dom(BaseCrmLocators.LOCATOR_LOADER)

    def user_input_in_field_to_change(self, name_user: list):
        """Ввод пользователя в поле поиска для смены"""
        with allure.step(f'Ввод пользователя в поле поиска для смены. user - {name_user}'):
            self.waiting_element_is_visibility_on_the_page(BaseCrmLocators.LOCATOR_UL_USER)
            self.expecting_clickability(BaseCrmLocators.LOCATOR_UL_USER)
            ul_user = self.find_element(BaseCrmLocators.LOCATOR_UL_USER)
            ul_user.click()
            self.waiting_element_is_visibility_located_dom(BaseCrmLocators.LOCATOR_INPUT_USER)
            self.expecting_clickability(BaseCrmLocators.LOCATOR_INPUT_USER)
            input_user = self.find_element(BaseCrmLocators.LOCATOR_INPUT_USER)
            input_user.send_keys(name_user[0])
            with allure.step('Ожидание появления элемента с именем искомого пользователя '
                             'в выпадающем списке пользователей для смены'):
                self.waiting_element_is_visibility_located_dom(BaseCrmLocators.LOCATOR_LI_SEARCH_USER)

    def click_user_change(self, name_user: list):
        """Смена пользователя"""
        with allure.step(f'Смена пользователя на ({name_user})'):
            self.click_button_testing_tools()
            self.click_button_change_for_yourself()
            self.user_input_in_field_to_change(name_user)

            user_busy = self.driver.find_elements(*BaseCrmLocators.LOCATOR_USER_BUSY)  # пользователь занят

            next_user = 1  # Номер пользователя в списке пользователей для согласования
            while len(user_busy) != 0:
                if next_user >= len(name_user):
                    print(
                        f'Все пользователи для согласования заняты!!! {name_user} - номер последнего пользователя в списке')
                    self.click_button_release_all_substitutions()
                    self.click_button_testing_tools()
                    self.user_input_in_field_to_change(name_user)
                    break

                input_user = self.find_element(BaseCrmLocators.LOCATOR_INPUT_USER)
                input_user.clear()
                input_user.send_keys(name_user[next_user])
                self.waiting_element_is_visibility_located_dom(BaseCrmLocators.LOCATOR_LI_SEARCH_USER)
                user_busy = self.driver.find_elements(*BaseCrmLocators.LOCATOR_USER_BUSY)
                next_user += 1
            with allure.step('Клик по элементу в выпадающем списке с найденным пользователем'):
                result_user = self.find_element(BaseCrmLocators.LOCATOR_RESULT_SEARCH_USER)
                result_user.click()
            with allure.step('Клик по кнопке Подмениться'):
                button_change = self.find_element(BaseCrmLocators.LOCATOR_BUTTON_CHANGE)
                button_change.click()

                with allure.step('Ожидание отработки лоадера'):
                    self.waiting_element_invisibility(BaseCrmLocators.LOCATOR_BUTTON_CHANGE)
                    time.sleep(1)
                    self.waiting_for_loader_processing_in_dom(BaseCrmLocators.LOCATOR_LOADER, sec=90)
                    self.waiting_for_loader_processing_in_dom(BaseCrmLocators.LOCATOR_LOADER_PQ)

    def change_for_yourself(self):
        """Смена на себя"""
        with allure.step('Смена на себя'):
            self.click_button_testing_tools()
            button_change_for_yourself = self.driver.find_elements(*BaseCrmLocators.LOCATOR_BUTTON_CHANGE_FOR_YOURSELF)
            if len(button_change_for_yourself) > 0:
                with allure.step('Клик по кнопке Подмениться на своего пользователя'):
                    self.expecting_clickability(BaseCrmLocators.LOCATOR_BUTTON_CHANGE_FOR_YOURSELF)
                    button_change_for_yourself[0].click()
                    time.sleep(2)
                    with allure.step('Ожидание отработки лоадера'):
                        self.waiting_element_invisibility(BaseCrmLocators.LOCATOR_BUTTON_CHANGE_FOR_YOURSELF)
                        self.waiting_for_loader_processing_in_dom(BaseCrmLocators.LOCATOR_LOADER)
                        self.waiting_element_is_visibility_located_dom(BaseCrmLocators.LOCATOR_BODY)
                        self.waiting_for_loader_processing_in_dom(BaseCrmLocators.LOCATOR_LOADER)

                # with allure.step('Очистка всех куки и обновление страницы'):
                #     action = ActionChains(self.driver)
                #     action.key_down(Keys.CONTROL).send_keys(Keys.F5).key_up(Keys.CONTROL).perform()
                #     time.sleep(3)
                #     with allure.step('Ожидание отработки лоадера'):
                #         self.waiting_for_loader_processing_in_dom(BaseCrmLocators.LOCATOR_LOADER)
                #     self.driver.delete_all_cookies()
                #     self.driver.refresh()
                #     time.sleep(3)
                # with allure.step('Ожидание отработки лоадера'):
                #     self.waiting_for_loader_processing_in_dom(BaseCrmLocators.LOCATOR_LOADER)
                #     time.sleep(2)

            else:
                with allure.step('Клик по кнопке Закрыть в модалке смены пользователя'):
                    self.expecting_clickability(ToolsLocators.LOCATOR_BUTTON_CLOSE)
                    button_close = self.find_element(ToolsLocators.LOCATOR_BUTTON_CLOSE)
                    button_close.click()
                    self.waiting_element_invisibility(BaseCrmLocators.LOCATOR_H4_TESTING_TOOLS)
