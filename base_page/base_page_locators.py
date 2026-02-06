# Базовый класс. В нем указываются локаторы, которые используются на всех страницах (типа лоадера)
from selenium.webdriver.common.by import By


class BaseOpenLocators:
    LOCATOR_SPINNER_NO_TEXT = (By.XPATH,
                               "//div[not(contains(@class, 'preloader-content__hide'))]/div[@class='spinner-border']")  # спиннер загрузки без текста
    LOCATOR_SPINNER_TEXT = (By.XPATH,
                            "//div[not(contains(@class, 'preloader-content__hide'))]/div[@class='spinner-border text-white']")  # Спиннер загрузки с текстом


# Базовые локаторы в CRM
class BaseCrmLocators:
    LOCATOR_BODY = (By.XPATH, "//body")
    LOCATOR_LOADER_TEXT = (By.XPATH, "//div[@class='dynamic-objects-loader']//div[@class='text-holder']"
                           )  # Лоадер с текстом
    LOCATOR_LOADER_ASSORTMENTS = (By.XPATH, "//div[@data-name='assortment']//div[@class='dynamic-objects-loader']"
                                  )  # Лоадер на странице Ассортимент
    LOCATOR_LOADER_RECOUNTING_KP = (
        By.XPATH, "//div[@class='dynamic-objects-loader']//div[@class='text-holder' and text()='Пересчет КП']"
    )  # Лоадер Пересчет КП
    LOCATOR_LOADER = (
        By.XPATH,
        "//div[@class='dynamic-objects-loader' and not(@style='display: none;')]//div[not(text()='Необходимо сохранить КП для определения согласований') and @class='loader']"
    )  # Лоадер без текста
    LOCATOR_LOADER_MODAL = (
        By.XPATH, "//div[@id='modal-container']//div[@class='dynamic-objects-loader']//div[@class='loader']"
    )  # Лоадер в модалке
    LOCATOR_LOADER_PQ = (
        By.XPATH, "//div[@id='main']//following::div[@class='loader'][last()]"
    )  # Лоадер на странице PQ
    LOCATOR_LOADER_TEXT_SAVE = (By.XPATH, "//div[@class='text-holder' and text()='Сохраняем...']"
                                )  # Лоадер с текстом "Сохранение..."

    # Локаторы модалки Смена пользователя
    LOCATOR_BUTTON_TESTING_TOOLS = (By.XPATH, "//a[@title='Инструменты тестирования']")  # Кнопка Смена пользователя
    LOCATOR_BUTTON_CHANGE_FOR_YOURSELF = (
        By.XPATH, "//p[text()='Подмениться на своего пользователя']")  # Кнопка Подмениться на себя
    LOCATOR_H4_TESTING_TOOLS = (
        By.XPATH, "//h4[text()='Инструменты тестирования']")  # Заголовок Инструменты тестирования
    LOCATOR_UL_USER = (
        By.XPATH, "//div[text()='Пользователь']/following-sibling::div"
    )  # Для вызова выпадающего списка для ввода пользователя
    LOCATOR_INPUT_USER = (By.XPATH, "//div[text()='Пользователь']/following::input[2]")  # Инпут для ввода пользователя
    LOCATOR_RESULT_SEARCH_USER = (
        By.XPATH, "//div[contains(text(), '(ridancorp')]")  # Пользователь для смены
    LOCATOR_LI_SEARCH_USER = (By.XPATH, "//li[@role='presentation']"
                              )  # Элемент выпадающего списка в поиске юзера для смены
    LOCATOR_BUTTON_CHANGE = (By.XPATH, "//p[text()='Подмениться']")  # Кнопка Подмениться
    LOCATOR_USER_BUSY = (By.XPATH, "//strong[contains(text(), 'Подменён на')]")  # Пользователь занят
    LOCATOR_INFO_MESSAGE = (By.XPATH, "//div[@class='noty_bar noty_type_warning']"
                            )  # Всплывающие информационные сообщения
    LOCATOR_BTN_RELEASE_ALL_SUBSTITUTIONS = (By.XPATH, "//div[@field='ResetAllUsersContext']//a"
                                             )  # Кнопка освободить все подмены
    LOCATOR_INFO_MSG_DISTRIBUTOR_IS_ASSIGNED = (
        By.XPATH, "//span[contains(text(), 'Дистрибьютор закреплен за инженерным разделом')]"
    )  # Всплывающее информационное сообщение Дистрибьютор закреплен за инженерным разделом


# Базовые локаторы 1с Ридан
class Base1cRidanLocators:
    LOCATOR_LOADER_SEARCH = (By.XPATH, "//div[text()='Поиск...']")  # Лоадер Поиск
    LOCATOR_DIV_CHANGE_NOTIFICATION = (By.XPATH, "//div[text()='Изменение:']")  # Всплывающее оповещение об изменении
