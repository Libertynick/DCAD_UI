import sys
import os.path

import allure
import psutil
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from datetime import datetime

from base_page.base_page import BasePage
from config import Options as optionConfig
from PIL import Image
import io

from tools import helper

sys.stdout.reconfigure(encoding='utf-8')


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Делаем скрины только при падении тестов"""
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed:
        test_name = os.environ.get('PYTEST_CURRENT_TEST'
                                   ).split('/')[-1].split('::')[0]  # получение имени запускаемого теста
        if optionConfig.PATH_TO_SCREENSHOT is not None:
            if os.path.exists(optionConfig.PATH_TO_SCREENSHOT):
                now = datetime.now()
                now_data = now.strftime("%d.%m.%y.%H.%M.%S")
                name_screenshot = f'{now_data}_{test_name}.png'
                try:
                    if 'browser' in item.fixturenames:  # Получаем экземпляр драйвера
                        web_driver = item.funcargs['browser']
                    else:
                        print('Fail to take screen-shot')
                        return

                    # Для скрина в отчете allure
                    attach = web_driver.get_screenshot_as_png()
                    allure.attach(attach, name_screenshot, attachment_type=allure.attachment_type.PNG)

                    path = optionConfig.PATH_TO_SCREENSHOT + name_screenshot
                    screen(web_driver, path)
                except Exception as e:
                    print("error on write screenshot")
                    print(optionConfig.PATH_TO_SCREENSHOT + name_screenshot)
                    print(e, '- ошибка')


def screen(browser, path):
    """Скриншот экрана не только видимой части экрана (со скролом страницы)"""

    total_height = browser.execute_script("return document.body.scrollHeight")
    size = browser.get_window_size()
    screenshot = Image.new('RGB', (size['width'], total_height))

    offset = 0
    while offset < total_height:
        browser.execute_script("window.scrollTo(0, %s);" % offset)
        screenshot.paste(Image.open(io.BytesIO(browser.get_screenshot_as_png())), (0, offset))
        # offset += 1080 # Вы можете изменить эту величину в зависимости от вашего экрана
        offset += size['height']  # Вы можете изменить эту величину в зависимости от вашего экрана
    screenshot.save(path, format='png')


def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default='chrome',
                     help="Choose driver: chrome or firefox")


def get_cpu_usage():
    # Получаем загрузку ЦП в процентах
    cpu_usage = psutil.cpu_percent(interval=1)  # Интервал в секундах
    print(f"Загруженность ЦП: {cpu_usage}%")


def get_memory_usage():
    # Получаем информацию о памяти
    memory = psutil.virtual_memory()
    memory_total = memory.total / (1024 ** 3)  # Перевод в гигабайты
    memory_used = memory.used / (1024 ** 3)  # Перевод в гигабайты
    memory_percent = memory.percent  # Процент использования

    print(f"Общая память: {memory_total:.2f} ГБ")
    print(f"Используемая память: {memory_used:.2f} ГБ")
    print(f"Загрузка памяти: {memory_percent}%")


def pytest_runtest_setup(item):
    """Получаем все маркировки теста"""
    markers = item.iter_markers()

    # for marker in markers:
    # print(f'Запуск теста "{item.name}" с маркировкой: {marker.name}')
    return markers


def get_markers(request) -> list:
    """
    Получение маркировок в тесте во время запуска
    :return: Список маркировок, используемых в тесте во время запуска
    """
    markers = request.node.iter_markers()
    markers = [marker.name for marker in markers]
    return markers


# для выгрузки всех артикулов из параметризации тестов. выгружаются даже просто при запуске pytest --collect-only
# def pytest_collection_modifyitems(config, items):
#     # Собираем артикулы из параметров тестов
#     articles = set()
#
#     for item in items:
#         # pytest хранит параметры в атрибуте callspec (если есть)
#         if hasattr(item, "callspec"):
#             # callspec.params — словарь параметров
#             params = item.callspec.params
#             # Предположим, параметр называется "article"
#             if "article" in params:
#                 articles.add(str(params["article"]))
#         else:
#             # Если параметризации нет — пропускаем
#             pass
#
#     # Сохраняем
#     with open("collected_articles.txt", "w") as f:
#         for art in sorted(articles):
#             f.write(art + "\n")
#
#     print(f"\n✅ Найдено {len(articles)} артикулов. Сохранены в collected_articles.txt")
#     # Опционально: принудительно завершить сбор, не запуская тесты
#     config.option.collectonly = True  # уже в режиме сбора, но можно явно


@pytest.fixture(scope='function')
def browser(request):
    browser_name = request.config.getoption('browser_name')
    options_add_experimental_option_detach = True  # не закрывать окно браузера по завершении теста (True - не закрывать)
    driver = None

    markers = get_markers(request)
    prod_marker = 'prod'  # Маркировка для тестов на проде

    if browser_name == 'chrome':
        get_cpu_usage()
        get_memory_usage()

        headless = 0  # Безголовый режим 0 - false
        user_agent = 'RIDAN_RND_TEST'

        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")  # отключить нативные уведомления браузера
        if prod_marker in markers:
            options.add_argument(f"user-agent={user_agent}")
        options.add_argument('--no-sandbox')
        options.add_argument("--log-level=3")
        options.add_argument(
            "--password-store=basic")  # отключает интеграцию с системным менеджером паролей (в т.ч. Google Password Manager).

        # Отключает встроенное уведомление об утечке паролей
        options.add_argument("--disable-password-leak-detection")
        options.add_argument("--disable-sync")  # Отключает синхронизацию с Google

        options.add_experimental_option('excludeSwitches', ['enable-logging', '--dns-prefetch-disable'])

        options.add_experimental_option("detach", options_add_experimental_option_detach
                                        )  # не закрывать окно браузера по завершении теста (True - не закрывать)
        prefs = {
            "profile.password_manager_leak_detection": False,
            'profile.default_content_setting_values.automatic_downloads': 1,
            'plugins.always_open_pdf_externally': True,  # It will not show PDF directly in chrome
            'profile.password_manager_enabled': False,  # Отключить менеджер паролей в хром
            'credentials_enable_service': False,  # Отключает службу сохранения и автозаполнения логинов/паролей,
            'profile.default_content_setting_values.notifications': 2,  # отключить уведомления
        }
        options.add_experimental_option("prefs", prefs)  # разрешение на скачивание нескольких файлов

        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

        if optionConfig.RUN_HEADLESS_BROWSER == '1':
            # options.add_argument("--headless")
            options.add_argument("--headless=new")
            headless = 1  # Безголовый режим 1 - true

        print('\nstart chrome driver for test...')

        #  При инициализации драйвера через менеджер драйвера
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # global driver
        driver = webdriver.Chrome(options=options)
        # При абсолютном пути драйвера
        # service = Service(executable_path=r'.\chrome_driver\chromedriver.exe')
        # driver = webdriver.Chrome(service=service, options=options)

        if headless == 1:
            driver.set_window_size(width=1920, height=1080)
        else:
            driver.maximize_window()

    yield driver

    expected_marker = 'stage'
    if expected_marker in markers:
        page_base = BasePage(driver, '')
        cookie = page_base.get_cookie_session()
        helper.release_all_substitutions_crm(cookie)
        print(f'Скинули все подмены при запуске теста с маркировкой {expected_marker}')

    print('\nquit driver..')
    # driver.close()
    # driver.quit()
