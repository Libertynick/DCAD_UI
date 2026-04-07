import allure
import pytest
from uuid import uuid4
from requests.exceptions import HTTPError

from api_testing_project.services.crm_commerce.full_commerce_new.api.api_full_commerce_new import FullCommerceNewApi
from api_testing_project.services.order.api.api_order_simulate import ApiOrderSimulate
from api_testing_project.services.order.payloads.payloads_order_simulate import PayloadsOrderSimulate
from api_testing_project.services.crm_commerce.create_offer.api.api_create_offer import ApiCreateOffer
from api_testing_project.services.crm_commerce.create_offer.payloads.payloads_create_offer import PayloadsCreateOffer
from api_testing_project.services.order.payloads.payloads_order_create import PayloadsOrderCreateWithOneCode
from api_testing_project.utils.offer_flow_helper import OfferFlowHelper
from api_testing_project.utils.full_commerce_new_validator import FullCommerceNewValidator
from api_testing_project.utils.full_commerce_new_validator import FullCommerceNewValidator


@pytest.mark.stage
@pytest.mark.dapi
@allure.feature('DAPI')
@allure.story('Негативные тесты на /api/CrmCommerce/FullCommerceNew')
class TestFullCommerceNewNegative:
    """
    Набор негативных тестов для метода /api/CrmCommerce/FullCommerceNew.

    Проверяет корректность обработки ошибочных ситуаций:
    - Невалидный формат requestId (не UUID)
    - Несуществующий requestId (валидный UUID, но отсутствует в БД)
    - Отсутствие обязательного параметра requestId

    Все тесты проверяют что API возвращает корректные коды ошибок
    и не падает при некорректных входных данных.
    """

    def setup_method(self):
        """
        Инициализация API класса перед каждым тестом.

        Создаёт экземпляр FullCommerceNewApi для выполнения запросов к API.
        """
        self.full_api = FullCommerceNewApi()

    @allure.title('FullCommerceNew с невалидным requestId - неправильный формат')
    @pytest.mark.stage
    def test_full_commerce_new_invalid_request_id_format(self):
        """
        Негативный тест: проверка поведения API при невалидном формате requestId.

        Тест отправляет GET запрос с requestId в неправильном формате (не UUID)
        и проверяет, что API корректно обрабатывает ошибку, возвращая HTTPError 400.

        Ожидаемый результат:
        - Получение HTTPError исключения
        - Статус код: 400 (Bad Request)
        """

        with allure.step('ШАГ 1: Отправляем GET запрос с невалидным requestId'):
            invalid_request_id = "invalid-uuid-format"
            print(f'Невалидный requestId: {invalid_request_id}')

        with allure.step('ШАГ 2: Проверяем что получаем HTTPError с кодом 400'):
            try:
                response = self.full_api.http_methods.get(
                    url=f'{self.full_api.endpoints.get_full_commerce_new(invalid_request_id)}'
                )
                assert False, f'Ожидалась ошибка HTTPError, но запрос выполнился успешно со статусом {response.status_code}'

            except HTTPError as e:
                print(f'Получена ожидаемая ошибка: {e}')
                print(f'Статус код: {e.response.status_code}')

                assert e.response.status_code == 400, \
                    f'Ожидался статус код 400 (Bad Request), получили {e.response.status_code}'

                print('Тест успешно выполнен')

    @allure.title('FullCommerceNew с несуществующим requestId')
    @pytest.mark.stage
    def test_full_commerce_new_non_existent_request_id(self):
        """
        Негативный тест: проверка поведения API при несуществующем requestId.

        Тест генерирует валидный UUID (который не существует в базе данных)
        и проверяет, что API корректно обрабатывает ситуацию, возвращая пустой результат.

        Ожидаемый результат:
        - Статус ответа: Ok, Warning или Error
        - Список objects: пустой (len = 0)
        """

        with allure.step('ШАГ 1: Генерируем несуществующий requestId'):
            non_existent_id = uuid4()
            print(f'Несуществующий requestId: {non_existent_id}')

        with allure.step('ШАГ 2: Отправляем GET запрос с несуществующим requestId'):
            response_data = self.full_api.get_full_commerce_new_by_request_id(non_existent_id)

        with allure.step('ШАГ 3: Проверяем структуру ответа'):
            print(f'Статус в ответе: {response_data.get("status")}')

            assert response_data.get('status') in ['Ok', 'Warning', 'Error'], \
                f'Неожиданный статус в ответе: {response_data.get("status")}'

            objects = response_data.get('objects', [])
            print(f'Количество объектов в ответе: {len(objects)}')

            assert len(objects) == 0, \
                f'Для несуществующего requestId ожидался пустой список objects, получили {len(objects)} объектов'

            print('Тест успешно выполнен')

    @allure.title('FullCommerceNew без параметра requestId')
    @pytest.mark.stage
    def test_full_commerce_new_without_request_id(self):
        """
        Негативный тест: проверка поведения API при отсутствии обязательного параметра requestId.

        Тест отправляет GET запрос без параметра requestId и проверяет,
        что API корректно обрабатывает ситуацию, возвращая пустой результат или статус Error.

        Ожидаемый результат:
        - Статус код: 200
        - Список objects: пустой (len = 0) ИЛИ статус ответа: Error
        """

        with allure.step('ШАГ 1: Отправляем GET запрос без параметра requestId'):
            base_url = str(self.full_api.endpoints.get_full_commerce_new('dummy')).rsplit('=', 1)[0]
            print(f'URL без параметра: {base_url}')

            response = self.full_api.http_methods.get(url=base_url)

        with allure.step('ШАГ 2: Проверяем статус код ответа'):
            print(f'Статус код: {response.status_code}')

            assert response.status_code == 200, \
                f'Ожидался статус код 200, получили {response.status_code}'

        with allure.step('ШАГ 3: Проверяем что в ответе пустой или некорректный результат'):
            response_data = response.json()
            print(f'Статус в ответе: {response_data.get("status")}')

            objects = response_data.get('objects', [])
            print(f'Количество объектов: {len(objects)}')

            assert len(objects) == 0 or response_data.get('status') == 'Error', \
                f'Ожидался пустой список objects или статус Error, получили {len(objects)} объектов со статусом {response_data.get("status")}'

            print('Тест успешно выполнен')


@pytest.mark.stage
@pytest.mark.dapi
@allure.feature('DAPI')
@allure.story('Позитивные тесты на /api/CrmCommerce/FullCommerceNew')
class TestFullCommerceNewPositive:
    """
    Набор позитивных тестов для метода /api/CrmCommerce/FullCommerceNew.

    Проверяет корректность работы метода FullCommerceNew в связке с CreateOffer
    для различных типов материалов (Material, BTP, HEX, Industrial).

    Каждый тест выполняет полный флоу:
    1. Simulate - получение информации о материале
    2. CreateOffer - создание коммерческого предложения
    3. FullCommerceNew - получение полной информации о КП
    4. Валидация всех полей ответа (data, details, deliveryOptions, permissions)

    Тесты проверяют что API корректно возвращает все необходимые данные
    и структура ответа соответствует ожидаемой.
    ВАЖНО!!! при накатке надо поменять поле "specificationId", берем его из объекта и самой верхней спецификации
    через дев тулсз забираем значением aria-controls
    """

    def setup_method(self):
        """
        Инициализация API классов перед каждым тестом.

        Создаёт экземпляры:
        - ApiOrderSimulate для работы с order/simulate
        - ApiCreateOffer для создания КП
        - FullCommerceNewApi для получения деталей КП
        """
        self.simulate_api = ApiOrderSimulate()
        self.create_offer_api = ApiCreateOffer()
        self.full_api = FullCommerceNewApi()

    @allure.title('CreateOffer -> FullCommerceNew для Material кода')
    @pytest.mark.stage
    def test_create_offer_to_full_commerce_new_material(self):
        """
        Тест флоу: Simulate -> CreateOffer -> FullCommerceNew для Material кода.

        Проверяет корректность работы метода FullCommerceNew для обычных торговых кодов.
        Тест выполняет полный цикл создания КП и проверки его деталей через FullCommerceNew.

        Шаги теста:
        1. Simulate - получение информации о материале
        2. Извлечение данных из Simulate для создания orderLines
        3. CreateOffer - создание коммерческого предложения
        4. FullCommerceNew - получение полной информации о КП
        5. Проверка структуры ответа (objects, data, details)
        6. Проверка основных полей в data
        7. Проверка основных полей в details
        8. Проверка наличия deliveryOptions
        9. Проверка наличия permissions
        """

        with allure.step('ШАГ 1: Simulate - получаем информацию о материале'):
            simulate_payload = PayloadsOrderSimulate.order_simulate_add_to_cart_material

            sim_resp = self.simulate_api.post_order_simulate(simulate_payload)
            print(f'Статус Simulate: {sim_resp.get("status")}')

            assert sim_resp.get('status') == 'Ok', \
                f'Simulate failed: {sim_resp.get("messages")}'

        with allure.step('ШАГ 2: Извлекаем данные из Simulate для создания orderLines'):
            order_lines = OfferFlowHelper.create_order_lines_from_simulate(sim_resp["objects"][0])
            material_code = order_lines[0]['materialCode']
            quantity = order_lines[0]['quantity']
            print(f'Материал: {material_code}')
            print(f'Количество: {quantity}')

        with allure.step('ШАГ 3: CreateOffer - создаем КП'):
            offer_payload = dict(PayloadsCreateOffer.base_valid_offer)
            offer_payload["orderLines"] = order_lines
            offer_payload["isDraft"] = False
            offer_payload.setdefault("paymentTerms", "RU00")
            offer_payload['userComment'] = 'ТЕСТ FullCommerceNew - Material'

            offer_resp = self.create_offer_api.post_create_offer(offer_payload)
            print(f'Статус CreateOffer: {offer_resp.get("status")}')

            assert offer_resp.get('status') == 'Ok', \
                f'CreateOffer failed: {offer_resp.get("messages")}'

            offers = offer_resp["objects"][0].get("offers") or []
            assert offers, 'CreateOffer: нет offers в ответе'

            offer_id = offers[0]["id"]
            offer_number = offers[0].get("number")
            print(f'Создан offer_id: {offer_id}')
            print(f'Номер оффера: {offer_number}')

        with allure.step('ШАГ 4: FullCommerceNew - получаем детали КП'):
            full_resp = self.full_api.get_full_commerce_new_by_request_id(offer_id)
            print(f'Статус FullCommerceNew: {full_resp.get("status")}')

            assert full_resp.get('status') == 'Ok', \
                f'FullCommerceNew failed: {full_resp.get("messages")}'

        with allure.step('ШАГ 5: Валидация FullCommerceNew через FullCommerceNewValidator'):
            validator = FullCommerceNewValidator(
                full_response=full_resp,
                create_offer_payload=offer_payload,
                create_offer_response=offer_resp,
                offer_id=offer_id,
                offer_number=offer_number
            )

            validator.verify_all_for_material(material_code, quantity)

        print('\nТест успешно выполнен')

    @allure.title('CreateOffer -> FullCommerceNew для BTP кода (проектные условия)')
    @pytest.mark.stage
    def test_create_offer_to_full_commerce_new_btp(self):
        """
        Тест флоу: Simulate -> CreateOffer -> FullCommerceNew для BTP кода.

        Проверяет корректность работы метода FullCommerceNew для производственных кодов (BTP).
        BTP требует создания КП с проектными условиями (personId, passportId, specTypeId, specificationId).

        Особенности BTP:
        - Используется deliveryOptionsProd вместо стандартного deliveryOptions
        - Обязательны проектные поля (passportId, specTypeId, specificationId)
        - lineType = 'BTP'

        Шаги теста:
        1. Simulate - получение информации о BTP материале
        2. Извлечение данных из Simulate для создания orderLines
        3. CreateOffer - создание КП с проектными условиями
        4. FullCommerceNew - получение полной информации о КП
        5. Проверка структуры ответа (objects, data, details)
        6. Проверка основных полей в data
        7. Проверка основных полей в details (lineType = BTP)
        8. Проверка наличия deliveryOptionsProd (специфично для BTP)
        9. Проверка проектных полей (passportId, specTypeId)
        10. Проверка наличия permissions
        """

        with allure.step('ШАГ 1: Simulate - получаем информацию о BTP материале'):
            simulate_payload = PayloadsOrderSimulate.order_simulate_add_to_cart_btp

            sim_resp = self.simulate_api.post_order_simulate(simulate_payload)
            print(f'Статус Simulate: {sim_resp.get("status")}')

            assert sim_resp.get('status') == 'Ok', \
                f'Simulate failed: {sim_resp.get("messages")}'

        with allure.step('ШАГ 2: Извлекаем данные из Simulate для создания orderLines'):
            order_lines = OfferFlowHelper.create_order_lines_from_simulate(sim_resp["objects"][0])
            material_code = order_lines[0]['materialCode']
            quantity = order_lines[0]['quantity']
            print(f'BTP материал: {material_code}')
            print(f'Количество: {quantity}')

        with allure.step('ШАГ 3: CreateOffer - создаем КП с проектными условиями для BTP'):
            offer_payload = dict(PayloadsCreateOffer.base_valid_offer)
            offer_payload["orderLines"] = order_lines
            offer_payload["isDraft"] = False
            offer_payload.setdefault("paymentTerms", "RU00")

            offer_payload['personId'] = '1c26afd2-1d97-4b7f-92fb-dd21ed412eea'
            offer_payload['passportId'] = '4dbb2a44-d895-468d-a51f-ae98b9b3d487'
            offer_payload['specTypeId'] = '02061701-51E6-402E-B18F-7BAE7A27F6FB'
            offer_payload['specificationId'] = 'bc9bee94-83e3-4402-bbf7-7558069384eb'

            if "deliveryOptions" in offer_payload:
                offer_payload["deliveryOptionsProd"] = offer_payload.pop("deliveryOptions")

            offer_payload['userComment'] = 'ТЕСТ FullCommerceNew - BTP с проектными условиями'

            print('Проектные поля:')
            print(f'  personId: {offer_payload["personId"]}')
            print(f'  passportId: {offer_payload["passportId"]}')
            print(f'  specTypeId: {offer_payload["specTypeId"]}')
            print(f'  specificationId: {offer_payload["specificationId"]}')

            offer_resp = self.create_offer_api.post_create_offer(offer_payload)
            print(f'Статус CreateOffer: {offer_resp.get("status")}')

            assert offer_resp.get('status') == 'Ok', \
                f'CreateOffer failed: {offer_resp.get("messages")}'

            offers = offer_resp["objects"][0].get("offers") or []
            assert offers, 'CreateOffer: нет offers в ответе'

            offer_id = offers[0]["id"]
            offer_number = offers[0].get("number")
            print(f'Создан offer_id: {offer_id}')
            print(f'Номер оффера: {offer_number}')

        with allure.step('ШАГ 4: FullCommerceNew - получаем детали КП для BTP'):
            full_resp = self.full_api.get_full_commerce_new_by_request_id(offer_id)
            print(f'Статус FullCommerceNew: {full_resp.get("status")}')

            assert full_resp.get('status') == 'Ok', \
                f'FullCommerceNew failed: {full_resp.get("messages")}'

        with allure.step('ШАГ 5: Валидация FullCommerceNew через FullCommerceNewValidator'):
            validator = FullCommerceNewValidator(
                full_response=full_resp,
                create_offer_payload=offer_payload,
                create_offer_response=offer_resp,
                offer_id=offer_id,
                offer_number=offer_number
            )

            validator.verify_all_for_btp(material_code, quantity)

        print('\nТест успешно выполнен для BTP с проектными условиями')

    @allure.title('CreateOffer -> FullCommerceNew для HEX кода (проектные условия)')
    @pytest.mark.stage
    def test_create_offer_to_full_commerce_new_hex(self):
        """
        Тест флоу: Simulate -> CreateOffer -> FullCommerceNew для HEX кода.

        Проверяет корректность работы метода FullCommerceNew для теплообменников (HEX).
        HEX требует создания КП с проектными условиями и deliveryOptionsDZRProd.

        Особенности HEX:
        - Используется deliveryOptionsDZRProd
        - Обязательны проектные поля (passportId, specTypeId, specificationId)
        - exchangeRateType = 'YRU' (проектные условия)
        - lineType = 'HEX'

        Шаги теста:
        1. Simulate - получение информации о HEX материале
        2. Извлечение данных из Simulate для создания orderLines
        3. CreateOffer - создание КП с проектными условиями
        4. FullCommerceNew - получение полной информации о КП
        5. Валидация через FullCommerceNewValidator
        """

        with allure.step('ШАГ 1: Simulate - получаем информацию о HEX материале'):
            simulate_payload = PayloadsOrderSimulate.order_simulate_add_to_cart_clover_hit

            sim_resp = self.simulate_api.post_order_simulate(simulate_payload)
            print(f'Статус Simulate: {sim_resp.get("status")}')

            assert sim_resp.get('status') == 'Ok', \
                f'Simulate failed: {sim_resp.get("messages")}'

        with allure.step('ШАГ 2: Извлекаем данные из Simulate для создания orderLines'):
            order_lines = OfferFlowHelper.create_order_lines_from_simulate(sim_resp["objects"][0])
            material_code = order_lines[0]['materialCode']
            quantity = order_lines[0]['quantity']
            print(f'HEX материал: {material_code}')
            print(f'Количество: {quantity}')

        with allure.step('ШАГ 3: CreateOffer - создаем КП с проектными условиями для HEX'):
            offer_payload = dict(PayloadsCreateOffer.base_valid_offer)
            offer_payload["orderLines"] = order_lines
            offer_payload["isDraft"] = True
            offer_payload.setdefault("paymentTerms", "RU00")

            offer_payload['personId'] = 'f8eaae4a-1309-4b24-95e8-3a092dc30067'
            offer_payload['passportId'] = '4dbb2a44-d895-468d-a51f-ae98b9b3d487'
            offer_payload['specTypeId'] = '02061701-51E6-402E-B18F-7BAE7A27F6FB'
            offer_payload['specificationId'] = 'bc9bee94-83e3-4402-bbf7-7558069384eb'
            offer_payload['exchangeRateType'] = 'YRU'
            offer_payload['currency'] = 'RUB'
            offer_payload['currencyDate'] = '2025-11-05T00:00:00'
            offer_payload['finalBuyerId'] = 'e55f3bae-ef45-43bd-b2f6-9f0148ca5622'
            offer_payload['customerId'] = 'acb8f425-c3b6-4b38-9f34-1e7fbfd53fa9'
            offer_payload['usePromoCurrency'] = True

            if "deliveryOptions" in offer_payload:
                offer_payload["deliveryOptionsDZRProd"] = offer_payload.pop("deliveryOptions")

            offer_payload['userComment'] = 'ТЕСТ FullCommerceNew - HEX с проектными условиями'

            print('Проектные поля:')
            print(f'  personId: {offer_payload["personId"]}')
            print(f'  passportId: {offer_payload["passportId"]}')
            print(f'  exchangeRateType: {offer_payload["exchangeRateType"]}')

            offer_resp = self.create_offer_api.post_create_offer(offer_payload)
            print(f'Статус CreateOffer: {offer_resp.get("status")}')

            assert offer_resp.get('status') == 'Ok', \
                f'CreateOffer failed: {offer_resp.get("messages")}'

            offers = offer_resp["objects"][0].get("offers") or []
            assert offers, 'CreateOffer: нет offers в ответе'

            offer_id = offers[0]["id"]
            offer_number = offers[0].get("number")
            print(f'Создан offer_id: {offer_id}')
            print(f'Номер оффера: {offer_number}')

        with allure.step('ШАГ 4: FullCommerceNew - получаем детали КП для HEX'):
            full_resp = self.full_api.get_full_commerce_new_by_request_id(offer_id)
            print(f'Статус FullCommerceNew: {full_resp.get("status")}')

            assert full_resp.get('status') == 'Ok', \
                f'FullCommerceNew failed: {full_resp.get("messages")}'

        with allure.step('ШАГ 5: Валидация FullCommerceNew через FullCommerceNewValidator'):
            validator = FullCommerceNewValidator(
                full_response=full_resp,
                create_offer_payload=offer_payload,
                create_offer_response=offer_resp,
                offer_id=offer_id,
                offer_number=offer_number
            )

            validator.verify_all_for_hex(material_code, quantity)

        print('\nТест успешно выполнен для HEX с проектными условиями')

    @allure.title('CreateOffer -> FullCommerceNew для Industrial кода (проектные условия)')
    @pytest.mark.stage
    def test_create_offer_to_full_commerce_new_industrial(self):
        """
        Тест флоу: Simulate -> CreateOffer -> FullCommerceNew для Industrial кода.

        Проверяет корректность работы метода FullCommerceNew для Industrial (HEX с проектными условиями).
        Industrial - это тот же HEX, но с дополнительными проектными параметрами.

        Особенности Industrial:
        - Используется deliveryOptionsDZRProd
        - Обязательны проектные поля (passportId, specTypeId, specificationId)
        - exchangeRateType = 'YRU' (проектные условия)
        - lineType = 'HEX'
        - Дополнительные поля: debtorAccount, clientInn

        Шаги теста:
        1. Simulate - получение информации об Industrial материале
        2. Извлечение данных из Simulate для создания orderLines
        3. CreateOffer - создание КП с проектными условиями
        4. FullCommerceNew - получение полной информации о КП
        5. Валидация через FullCommerceNewValidator
        """

        with allure.step('ШАГ 1: Simulate - получаем информацию об Industrial материале'):
            simulate_payload = PayloadsOrderSimulate.order_simulate_add_to_cart_industrial

            sim_resp = self.simulate_api.post_order_simulate(simulate_payload)
            print(f'Статус Simulate: {sim_resp.get("status")}')

            assert sim_resp.get('status') == 'Ok', \
                f'Simulate failed: {sim_resp.get("messages")}'

        with allure.step('ШАГ 2: Извлекаем данные из Simulate для создания orderLines'):
            order_lines = OfferFlowHelper.create_order_lines_from_simulate(sim_resp["objects"][0])
            material_code = order_lines[0]['materialCode']
            quantity = order_lines[0]['quantity']
            print(f'Industrial материал: {material_code}')
            print(f'Количество: {quantity}')

        with allure.step('ШАГ 3: CreateOffer - создаем КП с проектными условиями для Industrial'):
            offer_payload = dict(PayloadsCreateOffer.base_valid_offer)
            offer_payload["orderLines"] = order_lines
            offer_payload["isDraft"] = True
            offer_payload.setdefault("paymentTerms", "RU00")

            offer_payload['personId'] = 'b898f86a-6070-451b-9a14-47ba949c8cb8'
            offer_payload['passportId'] = '4dbb2a44-d895-468d-a51f-ae98b9b3d487'
            offer_payload['specTypeId'] = '02061701-51E6-402E-B18F-7BAE7A27F6FB'
            offer_payload['specificationId'] = 'bc9bee94-83e3-4402-bbf7-7558069384eb'
            offer_payload['exchangeRateType'] = 'YRU'
            offer_payload['currency'] = 'RUB'
            offer_payload['currencyDate'] = '2025-10-15T00:00:00'
            offer_payload['finalBuyerId'] = 'BF2FE82C-FED9-414B-9BA3-403CE76C9000'
            offer_payload['customerId'] = 'BF2FE82C-FED9-414B-9BA3-403CE76C9000'
            offer_payload['debtorAccount'] = '31/25-CH'
            offer_payload['clientInn'] = '5249173547'
            offer_payload['currencySpecialFixation'] = True
            offer_payload['setContractDiscounts'] = True

            if "deliveryOptions" in offer_payload:
                offer_payload["deliveryOptionsDZRProd"] = offer_payload.pop("deliveryOptions")

            offer_payload['userComment'] = 'ТЕСТ FullCommerceNew - Industrial с проектными условиями'

            print('Проектные поля:')
            print(f'  personId: {offer_payload["personId"]}')
            print(f'  passportId: {offer_payload["passportId"]}')
            print(f'  exchangeRateType: {offer_payload["exchangeRateType"]}')
            print(f'  debtorAccount: {offer_payload["debtorAccount"]}')

            offer_resp = self.create_offer_api.post_create_offer(offer_payload)
            print(f'Статус CreateOffer: {offer_resp.get("status")}')

            assert offer_resp.get('status') == 'Ok', \
                f'CreateOffer failed: {offer_resp.get("messages")}'

            offers = offer_resp["objects"][0].get("offers") or []
            assert offers, 'CreateOffer: нет offers в ответе'

            offer_id = offers[0]["id"]
            offer_number = offers[0].get("number")
            print(f'Создан offer_id: {offer_id}')
            print(f'Номер оффера: {offer_number}')

        with allure.step('ШАГ 4: FullCommerceNew - получаем детали КП для Industrial'):
            full_resp = self.full_api.get_full_commerce_new_by_request_id(offer_id)
            print(f'Статус FullCommerceNew: {full_resp.get("status")}')

            assert full_resp.get('status') == 'Ok', \
                f'FullCommerceNew failed: {full_resp.get("messages")}'

        with allure.step('ШАГ 5: Валидация FullCommerceNew через FullCommerceNewValidator'):
            validator = FullCommerceNewValidator(
                full_response=full_resp,
                create_offer_payload=offer_payload,
                create_offer_response=offer_resp,
                offer_id=offer_id,
                offer_number=offer_number
            )

            validator.verify_all_for_industrial(material_code, quantity)

        print('\nТест успешно выполнен для Industrial с проектными условиями')