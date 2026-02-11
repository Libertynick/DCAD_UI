import re
from typing import List, Any

import allure
from selenium.common import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tools.validators import assertions


class BaseElement:
    """
    Базовый элемент страницы
    Общие методы для взаимодействия с ui элементом страницы
    """

    def __init__(self, driver: WebDriver, locator: str, name: str):
        """
        :param driver: экземпляр веб драйвера
        :param locator: Строковое значение локатор
        :param name: Наименование элемента страницы
        """
        self.driver = driver
        self.locator = locator
        self.name = name

    @property
    def type_of(self):
        """
        Возвращает тип элемента. Переопределяется в потомках
        """
        return 'base_element'

    def get_locator(self, index: int = 0, **kwargs):
        """
        Формирует кортеж (By, value), используемый в Selenium.
        """
        with allure.step(f'Получение локатора {self.locator}'):
            formated_locator = self.locator.format(**kwargs)
            if index > 0:
                locator = f'({formated_locator})[{index}]'
            else:
                locator = formated_locator

            return By.XPATH, locator  # Можно использовать By.CSS и тд

    def find_element(self, index: int = 0, timeout: float = 10.0, **kwargs):
        """Поиск одного элемента"""
        with allure.step(f'Поиск элемента "{self.type_of} {self.name}"'):
            locator = self.get_locator(index=index, **kwargs)
            ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
            element = WebDriverWait(driver=self.driver, timeout=timeout, ignored_exceptions=ignored_exceptions
                                    ).until(EC.presence_of_element_located(locator),
                                            message=f"Не найден элемент '{self.type_of} {self.name}' по локатору {locator}")
            return element

    def find_elements(self, timeout: float = 10.0, **kwargs) -> list[WebElement]:
        """Поиск списка элементов"""
        with allure.step(f'Поиск элементов "{self.type_of} {self.name}"'):
            locator = self.get_locator(**kwargs)
            ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
            elements = WebDriverWait(driver=self.driver, timeout=timeout, ignored_exceptions=ignored_exceptions
                                     ).until(EC.presence_of_all_elements_located(locator),
                                             message=f"Не найдены элементы '{self.type_of} {self.name}' по локатору {locator}")
            return elements

    def find_elements_safely(self, timeout=0.5, **kwargs) -> List[WebElement]:
        try:
            return self.find_elements(timeout=timeout, **kwargs)
        except TimeoutException:
            return []

    def expecting_clickability(self, index: int = 0, timeout: float = 15.0, **kwargs):
        """Ожидание кликабельности элемента"""
        with allure.step(f'Ожидание кликабельности {self.type_of} {self.name}'):
            wait = WebDriverWait(self.driver, timeout)
            element = self.find_element(index=index, timeout=timeout, **kwargs)

            return wait.until(EC.element_to_be_clickable(element),
                              message=f'Элемент {self.type_of} {self.name} не кликабелен. Время ожидания - {timeout} сек.')

    def click(self, index: int = 0, timeout: float = 1.0, **kwargs):
        """
        Клик по элементу
        :param timeout: Время для ожидания кликабельности элемента
        :param index: Индекс элемента
        :param kwargs: Аргументы для форматирования локатора
        """
        with allure.step(f'Кликаем: "{self.type_of} {self.name}"'):
            element = self.find_element(index=index, timeout=timeout, **kwargs)
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.element_to_be_clickable(element),
                       message=f'Элемент "{self.type_of} {self.name}" не кликабелен. locator - {self.get_locator(index=index, **kwargs)}')
            element.click()

    def click_js(self, index: int = 0, timeout: float = 1.0, **kwargs):
        """
        Клик через javaScript
        :param timeout: Время для ожидания кликабельности элемента
        :param index: Индекс элемента
        :param kwargs: Аргументы для форматирования локатора
        """
        with allure.step(f'Кликаем с помощью js: {self.type_of} {self.name}'):
            element = self.find_element(index=index, timeout=timeout, **kwargs)
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.element_to_be_clickable(element),
                       message=f'Элемент "{self.type_of} {self.name}" не кликабелен')

            self.driver.execute_script("arguments[0].click()", element)

    def ctrl_click(self, index: int = 0, timeout: float = 1.0, **kwargs):
        """
        Ctrl+ click по элементу, открытие в новой вкладке
        :param timeout: Время для ожидания кликабельности элемента
        :param index: Индекс элемента
        :param kwargs: Аргументы для форматирования локатора
        """
        with allure.step(f'Ctrl+ click по {self.type_of} {self.name}, открытие в новой вкладке'):
            element = self.find_element(index=index, timeout=timeout, **kwargs)
            actions = ActionChains(self.driver)
            actions. \
                key_down(Keys.CONTROL) \
                .click(element) \
                .key_up(Keys.CONTROL) \
                .perform()

    def wait_visible_on_page(self, index: int = 0, timeout: float = 10.0, **kwargs):
        """Ожидание видимости элемента на странице"""
        with allure.step(f'Проверка видимости элемента "{self.type_of} {self.name}" на странице'):
            wait = WebDriverWait(self.driver, timeout)
            element = self.find_element(index=index, timeout=timeout, **kwargs)

            return wait.until(EC.visibility_of(element),
                              message=f'Элемент "{self.type_of} {self.name}" не виден на странице. Время ожидания - {timeout} сек.')

    def wait_presence_in_located_dom(self, index: int = 0, timeout: float = 10, **kwargs):
        """
        Ожидание появления элемента в DOM дереве
        :param timeout: Время ожидания
        :param index: Индекс элемента
        :param kwargs: Аргументы для форматирования локатора
        """
        with allure.step(f'Проверка появления в DOM дереве: {self.type_of} {self.name}'):
            locator = self.get_locator(index=index, **kwargs)
            wait = WebDriverWait(self.driver, timeout)

            return wait.until(EC.presence_of_element_located(locator),
                              message=f'Элемент "{self.type_of} {self.name}" не появился в DOM дереве. Время ожидания - {timeout} сек.')

    def wait_no_presence_in_located_dom(self, index: int = 0, timeout: float = 5, **kwargs):
        """
        Ожидание невидимости элемента в DOM дереве
        :param timeout: Время ожидания
        :param index: Индекс элемента
        :param kwargs: Аргументы для форматирования локатора
        """
        with allure.step(f'Проверка отсутствия "{self.type_of} {self.name}" в DOM дереве'):
            locator = self.get_locator(index=index, **kwargs)
            wait = WebDriverWait(self.driver, timeout)

            return wait.until(EC.invisibility_of_element_located(locator),
                              message=f'Элемент "{self.type_of} {self.name}" присутствует в DOM дереве. Время ожидания - {timeout} сек.')

    def wait_no_visible_on_page(self, index: int = 0, timeout: float = 10.0, **kwargs):
        """Ожидание невидимости элемента на странице"""
        with allure.step(f'Проверка невидимости элемента "{self.type_of} {self.name}" на странице'):
            wait = WebDriverWait(self.driver, timeout)
            locator = self.get_locator(index=index, **kwargs)

            return wait.until(EC.invisibility_of_element(locator),
                              message=f'Элемент "{self.type_of} {self.name}" виден на странице. Время ожидания {timeout} сек.')

    def should_text_in_element(self, expected_text: str, index: int = 0, **kwargs):
        """
        Должен быть определенный текст у элемента. Точное совпадение
        :param expected_text: Ожидаемый текст
        :param index: Индекс элемента
        """
        with allure.step(
                f'Проверка у элемента "{self.type_of} {self.name}" заданного текста- {expected_text}'):
            text_element = self.get_text_element(index=index, **kwargs)

            assertions.assert_eq(
                actual_value=text_element,
                expected_value=expected_text,
                allure_title=f'Сверяем текст в поле "{self.name}" с ожидаемым',
                error_message=f'Текст в "{self.type_of} {self.name}" не соответствует ожидаемому. '
                              f'На странице- {text_element}; ожидаемый текст- {expected_text}'
            )

    def should_text_in_list_elements(self, expected_text: str, **kwargs):
        """
        Должен быть определенный текст в списке элементов. Точное совпадение
        :param expected_text: Ожидаемый текст
        """
        with allure.step(
                f'Проверка у списка элементов "{self.type_of} {self.name}" заданного текста - ({expected_text})'):
            text_element = self.get_text_list_element(**kwargs)
            for el in text_element:
                assertions.assert_eq(
                    actual_value=el,
                    expected_value=expected_text,
                    allure_title=f'Сверяем текст в поле "{self.type_of} {self.name}" с ожидаемым',
                    error_message=f'Текст в "{self.type_of} {self.name}" не соответствует ожидаемому. '
                                  f'На странице- {el}; ожидаемый текст- {expected_text}'
                )

    def should_float_value_in_element(self, expected_value: float, index: int = 0, permissible_error: float = 1.0,
                                      **kwargs):
        """
        Должно быть определенное числовое значение (типа float) в поле. Проверяется разница в 1р.
        :param expected_value
        :param index: Индекс элемента
        :param permissible_error: Значение допустимой погрешности при сравнении
        :param kwargs: Аргументы для форматирования локатора
        """
        with (allure.step(
                f'Проверка числового значения у элемента "{self.type_of} {self.name}". Ожидаемое число {expected_value}. Проверяется разница в 1р.')):
            value_element_on_page = self.get_float_value_from_line(index=index, **kwargs)

            assertions.assert_eq_with_acceptable_error(
                actual_value=value_element_on_page,
                expected_value=expected_value,
                permissible_error=permissible_error,
                allure_title=f'Сравниваем число в поле "{self.name}" с ожидаемым',
                error_message=f'Числовое значение в поле "{self.type_of} {self.name}" не соответствует ожидаемому. '
                              f'На странице- {value_element_on_page}; ожидаемое- {expected_value}'
            )

    def should_contains_text_in_element(self, expected_contains_text: Any, index: int = 0, **kwargs):
        """
        Должно быть содержание текста в элементе
        :param expected_contains_text: Ожидаемое содержание текста
        :param index: Индекс элемента
        :param kwargs: Аргументы для форматирования локатора
        """
        with (allure.step(f'Проверка содержания текста у элемента "{self.type_of} {self.name}"')):
            text_element = self.get_text_element(index=index, **kwargs)

            assertions.assert_contains(
                actual_value=text_element,
                expected_contains=expected_contains_text,
                allure_title='Проверяем содержание ожидаемого текста в элементе',
                error_message=f'В элементе "{self.type_of} {self.name}" нет ожидаемого текста.'
                              f' На странице- {text_element} | ожидаемый- {expected_contains_text}'
            )

    def should_contains_text_not_symbol(self, expected_contains_text: Any, index: int = 0, **kwargs):
        """
        Должно быть содержание текста в элементе. Проверяется, отсекая все символы и цифры
        :param expected_contains_text: Ожидаемое содержание текста
        :param index: Индекс элемента
        :param kwargs: Аргументы для форматирования локатора
        """
        with allure.step(
                f'Проверка содержания сухого текста (текст без символов и цифр) у элемента "{self.type_of} {self.name}"'):
            text_element = self.get_text_element(index=index, **kwargs)
            text_element = ''.join(el for el in text_element if el.isalpha())

            assertions.assert_contains(
                actual_value=text_element,
                expected_contains=expected_contains_text,
                allure_title='Сверяем текста',
                error_message=f'В элементе {self.type_of} {self.name} нет ожидаемого текста - ({expected_contains_text}). '
                              f'Весь текст элемента - ({text_element})'
            )

    def should_contains_text_in_element_list(self, expected_contains_text: str, **kwargs):
        """
        Должно быть содержание текста в списке элементов
        :param expected_contains_text: Ожидаемое содержание текста
        :param kwargs: Аргументы для форматирования локатора
        """
        with (allure.step(f'Проверка содержания текста в списке элементов {self.type_of} {self.name}')):
            text_element_list = self.get_text_list_element(**kwargs)
            for el in text_element_list:
                assert expected_contains_text in el, \
                    (f'В элементе {self.type_of} {self.name} нет ожидаемого текста - ({expected_contains_text}). '
                     f'Весь текст элемента - ({el})')

    def should_not_special_text_in_element(self, text: str, index: int = 0, **kwargs):
        """
        Не должно быть определенного текста в элементе
        :param text: Текст, которого быть не должно
        :param index: Индекс элемента
        :param kwargs: Аргументы для форматирования локатора
        """
        with (allure.step(f'Проверка, что элемента "{self.type_of} {self.name}" нет определенного текста - {text}')):
            text_element = self.get_text_element(index=index, **kwargs)

            assertions.assert_not_eq(
                actual_value=text,
                value_not_eq=text_element,
                allure_title='Сравниваем текста',
                error_message=f'У элемента "{self.type_of} {self.name} есть текст ({text}). Весь текст элемента - ({text_element})"'
            )

    def check_is_not_empty_element(self, index: int = 0, **kwargs):
        """Проверка, что в элементе есть текст (не пустой)"""
        with allure.step(f'Проверка, что в элементе "{self.type_of} {self.name}" есть текст (не пустой)'):
            text_element = self.get_text_element(index=index, **kwargs)

            assertions.assert_not_eq(
                actual_value=text_element,
                value_not_eq='',
                allure_title='Сравниваем текста',
                error_message=f'В {self.type_of} {self.name} нет текста. Наполнение - ({text_element})'
            )

    def check_is_not_empty_element_list(self, **kwargs):
        """Проверка, что в списке элементов есть текст (не пустые)"""
        with allure.step(f'Проверка, что во всех элементах "{self.type_of} {self.name}" есть текст (не пустые)'):
            text_element_list = self.get_text_list_element(**kwargs)
            for el in text_element_list:
                assert el != '', f'В {self.type_of} {self.name} нет текста. Весь список с текстом - ({text_element_list})'

    def get_text_js(self, element: WebElement) -> str:
        """
        Получение текста через JS
        :param element: Найденный веб элемент DOM дерева
        :return: Текст веб элемента
        """
        text_element = self.driver.execute_script("return arguments[0].textContent;", element).strip()
        return text_element

    def get_text_element(self, index: int = 0, timeout: float = 3.0, **kwargs) -> str:
        """Получение текста у одного элемента"""
        with allure.step(f'Получение текста у "{self.type_of} {self.name}"'):
            element = self.find_element(index=index, timeout=timeout, **kwargs)
            text_element = element.text.strip()
            if text_element == '':
                text_element = self.get_text_js(element)
            return text_element

    def get_text_without_nesting(
            self,
            index: int = 0,
            allowed_tags: list[str] | None = None,
            **kwargs
    ) -> str:
        """
        Получить текст прямых дочерних узлов элемента, игнорируя вложенные элементы,
        кроме разрешённых тегов. Тег <br> автоматически заменяется на символ новой строки.

        :param index: Индекс элемента для поиска
        :param allowed_tags: Список тегов (в нижнем регистре), чей текст следует включать.
                             Например: ['span', 'b', 'i'].
                             Тег 'br' обрабатывается особым образом и не требует явного указания.
        :return: Объединённый текст прямых дочерних узлов.
        """
        if allowed_tags is None:
            allowed_tags = []

        # Приводим к нижнему регистру
        allowed_tags = [tag.lower() for tag in allowed_tags]

        with allure.step(f'Получить текст элемента {self.type_of} {self.name} без вложенных элементов '
                         f'(разрешённые теги: {allowed_tags or "нет"})'):
            element = self.find_element(index=index, **kwargs)
            text = self.driver.execute_script("""
                const allowedTags = arguments[1];
                let result = '';

                for (const node of arguments[0].childNodes) {
                    if (node.nodeType === Node.TEXT_NODE) {
                        result += node.textContent;
                    }
                    else if (node.nodeType === Node.ELEMENT_NODE) {
                        const tagName = node.tagName.toLowerCase();
                        if (tagName === 'br') {
                            result += '\\n';
                        }
                        else if (allowedTags.includes(tagName)) {
                            result += node.textContent;
                        }
                        // Иначе — игнорируем (не добавляем ничего)
                    }
                }

                // Удаляем пробелы по краям, но сохраняем внутренние переносы
                return result.trim();
            """, element, allowed_tags)

            return text

    def get_text_without_nesting_in_list_element(self, **kwargs) -> list[str]:
        """
        Получить текст без текста вложенных элементов из списка элементов
        :return: Текст веб элемента без вложенных в него элементов
        """
        with allure.step(
                f'Получить текст из списка элементов {self.type_of} {self.name} без текста вложенных элементов'):
            elements = self.find_elements(**kwargs)
            list_text = []
            for element in elements:
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
                list_text.append(text)
            return list_text

    def get_text_list_element(self, **kwargs) -> list[str]:
        """Получение текста из списка элементов"""
        with allure.step(f'Получение текста из списка элементов "{self.type_of} {self.name}"'):
            list_element = self.find_elements(**kwargs)
            list_element = [self.get_text_js(el) for el in list_element]
            return list_element

    def get_attribute_by_name(self, name_attribute: str, index: int = 0, **kwargs) -> str:
        """
        Получить атрибут элемента по наименованию
        :param name_attribute: Наименование искомого атрибута
        :param index: Индекс элемента
        """
        with allure.step(f'Получить атрибут элемента "{self.type_of} {self.name}" по наименованию {name_attribute}'):
            element = self.find_element(index=index, **kwargs)
            attribute_element = element.get_attribute(name_attribute)
            return attribute_element

    def scroll_to_elem_action_chains(self, index: int = 0, timeout: float = 1.0, **kwargs):
        """Прокрутка страницы до элемента с помощью ActionChains"""
        element = self.find_element(index=index, timeout=timeout, **kwargs)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

    def scroll_to_elem_js(self, index: int = 0, timeout: float = 1.0, **kwargs):
        """Прокрутка страницы до элемента с помощью js"""
        with allure.step('Прокрутка страницы до элемента'):
            element = self.find_element(index=index, timeout=timeout, **kwargs)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});", element)

    def get_float_value_from_line(self, index: int = 0, **kwargs) -> float:
        """
        Получить число типа float из строки. Часто используется для извлечения итоговой стоимости или скидки
        :param index: Индекс найденного элемента
        :param kwargs: Аргументы для форматирования локатора
        :return: Число типа float
        """
        with allure.step(f'Извлекаем число из {self.type_of} {self.name}'):
            text_element = self.get_text_element(index=index, **kwargs)
            text_element = text_element.replace('у.е.', '').replace('₽', '')
            # Удаляем завершающую точку, если она есть и не является частью числа
            if text_element.endswith('.'):
                text_element = text_element[:-1].rstrip()
            value_float = re.sub(r'[^\d,.]', '', text_element)  # Оставляем только цифры и запятую
            value_float = value_float.replace(',', '.')
            return float(value_float)

    def get_float_value_without_nesting_from_line(self, index: int = 0, **kwargs) -> float:
        """
        Получить число типа float из строки без текста, вложенного в элемент. Часто используется для извлечения итоговой стоимости или скидки
        :param index: Индекс найденного элемента
        :param kwargs: Аргументы для форматирования локатора
        :return: Число типа float
        """
        with allure.step(f'Извлекаем число из {self.type_of} {self.name}. Не берем вложенные в него элементы'):
            element = self.find_element(index=index, **kwargs)
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

            text_element = text.replace('у.е.', '')
            # Удаляем завершающую точку, если она есть и не является частью числа
            if text_element.endswith('.'):
                text_element = text_element[:-1].rstrip()
            value = re.sub(r'[^\d,.]', '', text_element)  # Оставляем только цифры и запятую
            value_float = float(value.replace(',', '.'))
            return value_float

    def get_float_value_from_all_line(self, **kwargs) -> list[float]:
        """
        Получить число типа float из списка строк. Часто используется для извлечения итоговой стоимости или скидки
        :return: Значение типа list, в котором хранятся числа типа float
        """
        with allure.step(f'Извлекаем число из списка элементов {self.type_of} {self.name}'):
            text_element = self.get_text_list_element(**kwargs)
            value_float = []
            for el in text_element:
                el = el.replace(',', '.')
                value_float.append(float(re.sub(r'[^0-9.]+', r'', el)))

            return value_float

    def double_click(self, index: int = 0, timeout: float = 1.0, **kwargs):
        """Двойной клик по элементу"""
        with allure.step(f'Двойной клик по "{self.type_of} {self.name}"'):
            action_chans = ActionChains(self.driver)

            element = self.find_element(index=index, timeout=timeout, **kwargs)
            action_chans.double_click(element).perform()

    def right_click(self, index: int = 0, timeout: float = 1.0, **kwargs):
        """Клик правой кнопкой мыши
        web_element - найденный элемент на странице
        """
        with allure.step(f'Клик правой кнопкой мыши по "{self.type_of} {self.name}"'):
            element = self.find_element(index=index, timeout=timeout, **kwargs)
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.element_to_be_clickable(element),
                       message=f'Элемент "{self.type_of} {self.name}" не кликабелен. locator - {self.get_locator(index=index, **kwargs)}')

            action = ActionChains(self.driver)
            action.context_click(element).perform()
