import allure
import pytest
from datetime import datetime
from typing import Dict, Callable

from api_testing_project.services.order.api.api_update_order_in_one_crm import ApiUpdateOrderInOneCrm
from api_testing_project.services.order.models.update_order_in_one_crm_model import UpdateOrderInOneCrmModel
from api_testing_project.services.order.payloads.payloads_update_order_in_one_crm import PayloadsUpdateOrderInOneCrm


@pytest.mark.stage
@pytest.mark.dapi
@allure.feature("DAPI")
@allure.story("UpdateOrderInOneCrm - Параметризованные тесты")
class TestUpdateOrderInOneCrmParametrized:
    """
    Набор параметризованных тестов для метода /api/Offer/UpdateOrderInOneCrm

    Класс содержит позитивные и негативные тесты для проверки обновления заказа.
    Все тесты используют параметризацию для проверки различных сценариев обновления.

    ВАЖНО: При обновлении базы (прода на тест), нужно поменять три параметра в get_base_payload
    "ODID" - бере руками из офера в срм, заходим в две тулз , далее в пейлоад и из сегмента materials
     берем ODID
     "DocumentNumber" - номер заказа
     "QuotationNumber" - номер ДКП

    Структура тестов:
        - Позитивные тесты: 5 тестов на успешное обновление различных полей заказа
        - Негативные тесты: 3 теста на обработку отсутствующих обязательных полей
    """

    def setup_method(self):
        """
        Инициализация перед каждым тестом

        Создает экземпляр API класса для работы с методом UpdateOrderInOneCrm.
        Этот метод автоматически вызывается pytest перед каждым тестом.
        """
        self.update_order_api = ApiUpdateOrderInOneCrm()

    @allure.title("ПОЗИТИВНЫЙ ТЕСТ: {test_name}")
    @pytest.mark.parametrize(
        "test_name, payload_method, fields_to_check, expected_status",
        [
            (
                    "Обновление дат и комментариев",
                    lambda: PayloadsUpdateOrderInOneCrm.update_dates_and_comments(
                        PayloadsUpdateOrderInOneCrm.get_base_payload()
                    ),
                    ["Date", "ReferenceDate", "ClientCommen", "AddlInfo"],
                    "Ok"
            ),
            (
                    "Обновление информации о доставке",
                    lambda: PayloadsUpdateOrderInOneCrm.update_delivery_info(
                        PayloadsUpdateOrderInOneCrm.get_base_payload(),
                        delivery_address="г. Москва, ул. Тестовая, д. 123",
                        contact_person="Тестовый Пользователь",
                        delivery_partner="СДЭК"
                    ),
                    ["DeliveryAddress", "ContactPerson", "DeliveryPartner"],
                    "Ok"
            ),
            (
                    "Обновление финансовых полей",
                    lambda: PayloadsUpdateOrderInOneCrm.update_financial_fields(
                        PayloadsUpdateOrderInOneCrm.get_base_payload(),
                        prepay_amount=2000.00,
                        delivery_cost=500.00,
                        discount_value=100.00
                    ),
                    ["PrepayAmountToCollect", "DeliveryCost", "DelayedDeliveryDiscountValue"],
                    "Ok"
            ),
            (
                    "Обновление только комментариев без изменения дат",
                    lambda: PayloadsUpdateOrderInOneCrm.update_dates_and_comments(
                        PayloadsUpdateOrderInOneCrm.get_base_payload(),
                        update_dates=False,
                        update_comments=True,
                        custom_comment="Пользовательский комментарий для теста",
                        custom_addl_info="Дополнительная информация для теста"
                    ),
                    ["ClientCommen", "AddlInfo"],
                    "Ok"
            ),
            (
                    "Обновление только контактного лица",
                    lambda: PayloadsUpdateOrderInOneCrm.update_delivery_info(
                        PayloadsUpdateOrderInOneCrm.get_base_payload(),
                        contact_person="Новое Контактное Лицо"
                    ),
                    ["ContactPerson"],
                    "Ok"
            ),
        ],
        ids=[
            "positive_update_dates_and_comments",
            "positive_update_delivery_info",
            "positive_update_financial_fields",
            "positive_update_comments_only",
            "positive_update_contact_person_only"
        ]
    )
    def test_positive_update_order(
            self,
            test_name: str,
            payload_method: Callable,
            fields_to_check: list,
            expected_status: str
    ):
        """
        Позитивные тесты обновления заказа

        Проверяет успешное обновление различных полей заказа.
        Каждый тест отправляет запрос с измененными данными и проверяет,
        что API возвращает успешный ответ.

        :param test_name: Название тестового сценария (отображается в отчете)
        :param payload_method: Функция, возвращающая подготовленный payload
        :param fields_to_check: Список полей, которые были изменены (для логирования)
        :param expected_status: Ожидаемый статус ответа ("Ok")

        Шаги теста:
            1. Получение базового payload для заказа
            2. Применение изменений к указанным полям
            3. Отправка запроса на обновление заказа
            4. Проверка статуса ответа
            5. Проверка наличия данных обновленного заказа
            6. Вывод информации об успешном обновлении

        Ожидаемый результат:
            - Статус ответа: "Ok"
            - В ответе есть объект с данными заказа
            - Заказ успешно обновлен
        """
        with allure.step(f"Шаг 1: Подготовка payload для теста '{test_name}'"):
            update_payload = payload_method()
            print("\n" + "=" * 80)
            print(f"ТЕСТ: {test_name}")
            print("=" * 80)
            print(f"Заказ для обновления")
            print(f"Коммерческое предложение: PQ04813171-1")
            print(f"Изменяемые поля: {', '.join(fields_to_check)}")
            print("=" * 80)

        with allure.step("Шаг 2: Вывод изменяемых полей"):
            print("\nИЗМЕНЯЕМЫЕ ПОЛЯ:")
            for field in fields_to_check:
                if field in update_payload:
                    print(f"  - {field}: {update_payload[field]}")
                else:
                    print(f"  - {field}: (вложенное поле или не найдено на верхнем уровне)")

        with allure.step("Шаг 3: Отправка POST запроса на /api/Offer/UpdateOrderInOneCrm"):
            print("\n" + "=" * 80)
            print("ОТПРАВКА ЗАПРОСА...")
            print("=" * 80)
            update_response = self.update_order_api.post_update_order_in_one_crm(update_payload)
            print(f"\nОтвет получен. Статус: {update_response.get('status')}")

        with allure.step("Шаг 4: Валидация ответа через Pydantic модель"):
            print("\nВАЛИДАЦИЯ ОТВЕТА...")
            result = UpdateOrderInOneCrmModel(**update_response)
            print(f"✓ Ответ успешно провалидирован через Pydantic модель")

        with allure.step(f"Шаг 5: Проверка статуса ответа (ожидается '{expected_status}')"):
            print(f"\nПроверка статуса: {result.status.value}")
            assert result.status.value == expected_status, \
                f"Ожидался статус '{expected_status}', получен '{result.status.value}'. Сообщения: {result.messages}"
            print(f"✓ Статус корректный: {result.status.value}")

        with allure.step("Шаг 6: Проверка наличия объектов в ответе"):
            print(f"\nПроверка наличия objects в ответе...")
            assert result.objects, "В ответе отсутствуют объекты (objects пустой)"
            print(f"✓ Найдено объектов: {len(result.objects)}")

        with allure.step("Шаг 7: Получение данных обновленного заказа"):
            updated_order = result.objects[0]
            print("\n" + "=" * 80)
            print("РЕЗУЛЬТАТ ОБНОВЛЕНИЯ:")
            print("=" * 80)
            print(f"Номер заказа: {updated_order.order_number}")
            print(f"Offer ID: {updated_order.offer_id}")
            print(f"Offer Number: {updated_order.offer_number}")
            print("=" * 80)

        with allure.step("✓ ТЕСТ УСПЕШНО ЗАВЕРШЕН"):
            print("\n" + "=" * 80)
            print(f"✓ ТЕСТ '{test_name}' УСПЕШНО ПРОЙДЕН!")
            print("=" * 80 + "\n")

    @allure.title("НЕГАТИВНЫЙ ТЕСТ: {test_name}")
    @pytest.mark.parametrize(
        "test_name, payload_method, expected_status, error_description",
        [
            (
                    "Отсутствует обязательное поле DocumentNumber",
                    PayloadsUpdateOrderInOneCrm.negative_missing_document_number,
                    "Error",
                    "API должен вернуть ошибку, т.к. без номера заказа невозможно определить какой заказ обновлять"
            ),
            (
                    "Отсутствует обязательное поле QuotationNumber",
                    PayloadsUpdateOrderInOneCrm.negative_missing_quotation_number,
                    "Error",
                    "API должен вернуть ошибку, т.к. заказ должен быть привязан к коммерческому предложению"
            ),
            (
                    "Отсутствует объект Organization",
                    PayloadsUpdateOrderInOneCrm.negative_missing_organization,
                    "Error",
                    "API должен вернуть ошибку, т.к. необходимо указать организацию-контрагента"
            ),
        ],
        ids=[
            "negative_missing_document_number",
            "negative_missing_quotation_number",
            "negative_missing_organization"
        ]
    )
    def test_negative_update_order(
            self,
            test_name: str,
            payload_method: Callable,
            expected_status: str,
            error_description: str
    ):
        """
        Негативные тесты обновления заказа

        Проверяет корректную обработку ошибочных данных при попытке обновления заказа.
        Каждый тест отправляет запрос с некорректными данными и проверяет,
        что API возвращает ошибку с соответствующим статусом.

        :param test_name: Название негативного сценария (отображается в отчете)
        :param payload_method: Функция, возвращающая некорректный payload
        :param expected_status: Ожидаемый статус ответа ("Error")
        :param error_description: Описание ожидаемой ошибки

        Шаги теста:
            1. Подготовка некорректного payload
            2. Отправка запроса на обновление заказа
            3. Проверка, что API вернул ошибку
            4. Проверка статуса ответа
            5. Вывод информации об ошибке

        Ожидаемый результат:
            - Статус ответа: "Error" или HTTP 400
            - В ответе есть сообщение об ошибке
            - Заказ не был обновлен
        """
        with allure.step(f"Шаг 1: Подготовка некорректного payload для теста '{test_name}'"):
            update_payload = payload_method()
            print("\n" + "=" * 80)
            print(f"НЕГАТИВНЫЙ ТЕСТ: {test_name}")
            print("=" * 80)
            print(f"Описание: {error_description}")
            print(f"Ожидаемый результат: Ошибка от API")
            print("=" * 80)

        with allure.step("Шаг 2: Отправка POST запроса на /api/Offer/UpdateOrderInOneCrm"):
            print("\n" + "=" * 80)
            print("ОТПРАВКА ЗАПРОСА С НЕКОРРЕКТНЫМИ ДАННЫМИ...")
            print("=" * 80)

            try:
                update_response = self.update_order_api.post_update_order_in_one_crm(update_payload)
                request_succeeded = True
                print(f"\nОтвет получен (HTTP 200)")
            except Exception as e:
                request_succeeded = False
                update_response = None
                error_exception = e
                print(f"\nПолучено исключение: {type(e).__name__}")
                print(f"Сообщение: {str(e)}")

        with allure.step("Шаг 3: Анализ типа ошибки"):
            print("\nТИП ОТВЕТА:")

            if not request_succeeded:
                response_type = f"Исключение {type(error_exception).__name__}"
                print(f"  Тип: {response_type}")
                print(f"  Это ожидаемое поведение для негативного теста")
            elif isinstance(update_response, dict) and "status" in update_response:
                response_type = "UpdateOrderInOneCrm модель (status/messages/objects)"
                print(f"  Тип: {response_type}")
                print(f"  Статус: {update_response.get('status')}")
            elif isinstance(update_response, dict) and "errors" in update_response:
                response_type = "ASP.NET Core Validation Error (HTTP 400)"
                print(f"  Тип: {response_type}")
                print(f"  HTTP Status: {update_response.get('status', 400)}")
                print(f"  Title: {update_response.get('title')}")
            else:
                response_type = "Неизвестный формат ответа"
                print(f"  Тип: {response_type}")

        with allure.step("Шаг 4: Проверка что API вернул ошибку"):
            error_detected = False
            error_messages = []

            if not request_succeeded:
                error_detected = True
                error_messages.append(str(error_exception))
                print(f"\n✓ API вернул ошибку через исключение")
                print(f"✓ Тип исключения: {type(error_exception).__name__}")

            elif isinstance(update_response, dict):
                if "status" in update_response:
                    result = UpdateOrderInOneCrmModel(**update_response)
                    print(f"\nВалидация через Pydantic модель успешна")
                    print(f"Статус: {result.status.value}")

                    if result.status.value == "Error":
                        error_detected = True
                        error_messages = result.messages
                        print(f"✓ API вернул статус 'Error'")
                    else:
                        print(f"✗ Ожидался статус 'Error', получен '{result.status.value}'")

                elif "errors" in update_response:
                    error_detected = True
                    print(f"✓ API вернул HTTP 400 с валидационными ошибками")

                    errors_dict = update_response.get("errors", {})
                    for field, messages in errors_dict.items():
                        if isinstance(messages, list):
                            error_messages.extend([f"{field}: {msg}" for msg in messages])
                        else:
                            error_messages.append(f"{field}: {messages}")

            assert error_detected, \
                f"API не вернул ошибку. Ответ: {update_response}"

            print(f"✓ Ошибка успешно обнаружена")

        with allure.step("Шаг 5: Вывод сообщений об ошибке"):
            print("\n" + "=" * 80)
            print("СООБЩЕНИЯ ОБ ОШИБКЕ ОТ API:")
            print("=" * 80)
            if error_messages:
                for idx, message in enumerate(error_messages, 1):
                    print(f"{idx}. {message}")
            else:
                print("Сообщения отсутствуют (но ошибка обнаружена по другим признакам)")
            print("=" * 80)

        with allure.step("✓ НЕГАТИВНЫЙ ТЕСТ УСПЕШНО ЗАВЕРШЕН"):
            print("\n" + "=" * 80)
            print(f"✓ НЕГАТИВНЫЙ ТЕСТ '{test_name}' УСПЕШНО ПРОЙДЕН!")
            print(f"✓ API корректно обработал некорректные данные и вернул ошибку")
            print(f"✓ Тип ошибки: {response_type}")
            print("=" * 80 + "\n")