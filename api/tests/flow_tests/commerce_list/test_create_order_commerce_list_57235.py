import copy

import allure
import pytest

from api_testing_project.services.order.api.api_order_simulate import ApiOrderSimulate
from api_testing_project.services.order.payloads.payloads_order_simulate import PayloadsOrderSimulate
from api_testing_project.services.crm_commerce.create_offer.api.api_create_offer import ApiCreateOffer
from api_testing_project.services.crm_commerce.create_offer.payloads.payloads_create_offer import PayloadsCreateOffer
from api_testing_project.services.crm_commerce.full_commerce_new.api.api_full_commerce_new import FullCommerceNewApi
from api_testing_project.services.order.api.api_order_create import ApiOrderCreate
from api_testing_project.services.order.payloads.payloads_order_create import PayloadsOrderCreateWithOneCode
from api_testing_project.services.crm_commerce.commerce_list.api.api_commerce_list import ApiCommerceList
from api_testing_project.services.crm_commerce.commerce_list.payloads.commerce_list import PayloadsCommerceList
from api_testing_project.services.crm_commerce.commerce_list.models.commerce_list import CommerceListModel


@pytest.mark.stage
@pytest.mark.dapi
@allure.feature("DAPI")
@allure.story("Simulate -> CreateOffer -> Order/Create -> CommerceList")
class TestCommerceList:

    def setup_method(self):
        self.simulate_api = ApiOrderSimulate()
        self.create_offer_api = ApiCreateOffer()
        self.full_api = FullCommerceNewApi()
        self.order_create_api = ApiOrderCreate()
        self.commerce_list_api = ApiCommerceList()

    @allure.title('Тест на CommerceList: создание заказа и проверка его в списке')
    @pytest.mark.stage
    def test_commerce_list_with_created_order_57235(self):

        with allure.step("Шаг 1: POST /api/Order/Simulate"):
            print("\nШАГ 1: SIMULATE - Получаем данные о материале")

            simulate_payload = copy.deepcopy(dict(PayloadsOrderSimulate.order_simulate_add_to_cart_material))
            simulate_payload['materials'][0]['quantity'] = 2

            simulate_response = self.simulate_api.post_order_simulate(simulate_payload)

            print(f"Simulate response status: {simulate_response.get('status')}")

            assert simulate_response.get('status') == 'Ok', \
                f"Simulate failed: {simulate_response.get('messages')}"

            order_lines = self.simulate_api.get_list_order_lines()
            assert order_lines, "Simulate: нет orderLines"

            material_code = order_lines[0].material_code
            original_quantity = order_lines[0].ordered_quantity
            line_type = order_lines[0].line_type

            print(f"Материал: {material_code}")
            print(f"Количество: {original_quantity}")

        with allure.step("Шаг 2: POST /api/CrmCommerce/CreateOffer"):
            print("\nШАГ 2: CREATE OFFER - Создаём КП")

            create_offer_payload = dict(PayloadsCreateOffer.base_valid_offer)
            create_offer_payload['isDraft'] = False
            create_offer_payload['orderLines'] = [
                {
                    'materialCode': material_code,
                    'quantity': original_quantity,
                    'lineNumber': 1,
                    'lineType': line_type
                }
            ]

            create_offer_response = self.create_offer_api.post_create_offer(create_offer_payload)

            print(f"CreateOffer response status: {create_offer_response.get('status')}")

            assert create_offer_response.get('status') == 'Ok', \
                f"CreateOffer failed: {create_offer_response.get('messages')}"

            offers = create_offer_response["objects"][0].get("offers") or []
            assert offers, f"CreateOffer: нет offers в ответе"

            offer_id = offers[0]["id"]
            offer_number = offers[0]["number"]

            print(f"Создан оффер ID: {offer_id}")
            print(f"Номер оффера: {offer_number}")

        with allure.step("Шаг 3: GET /api/CrmCommerce/FullCommerceNew"):
            print("\nШАГ 3: FULL COMMERCE NEW - Получаем ODID")

            full_response = self.full_api.get_full_commerce_new_by_request_id(offer_id)

            assert full_response.get('status') == 'Ok', \
                f"FullCommerceNew failed: {full_response.get('messages')}"

            details = full_response["objects"][0].get("details", [])
            assert details, "FullCommerceNew: нет details"

            odid = details[0].get("id")
            print(f"ODID первой позиции: {odid}")

        with allure.step("Шаг 4: POST /api/Order/Create"):
            print("\nШАГ 4: ORDER CREATE - Создаём заказ")

            order_create_payload = dict(
                PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_materials_prepayment_pickup)
            order_create_payload['orderLines'] = [
                {
                    'materialCode': material_code,
                    'quantity': original_quantity,
                    'lineNumber': 1,
                    'odid': str(odid),
                    'lineType': line_type,
                    'requestedMaterialCode': None,
                    'excludePosition': False
                }
            ]
            order_create_payload['offerId'] = str(offer_id)

            order_create_response = self.order_create_api.post_order_create(order_create_payload)

            print(f"Order/Create response status: {order_create_response.get('status')}")

            assert order_create_response.get('status') == 'Ok', \
                f"Order/Create failed: {order_create_response.get('messages')}"

            order_objects = order_create_response.get('objects', [])
            assert order_objects, "Order/Create: нет objects"

            orders = order_objects[0].get('orders', [])
            assert orders, "Order/Create: нет orders"

            created_offer_number = orders[0].get('offerNumber')

            print(f"Создан заказ с номером: {created_offer_number}")

        with allure.step("Шаг 5: POST /api/CrmCommerce/CommerceList"):
            print("\nШАГ 5: COMMERCE LIST - Проверяем что заказ есть в списке")

            commerce_list_payload = PayloadsCommerceList.get_commerce_list_payload()

            commerce_list_response = self.commerce_list_api.post_commerce_list(commerce_list_payload)

            print(f"CommerceList response status: {commerce_list_response.get('status')}")

            assert commerce_list_response.get('status') == 'Ok', \
                f"CommerceList failed: {commerce_list_response.get('messages')}"

            result = CommerceListModel(**commerce_list_response)

            offers_list = result.objects[0].offers

            print(f"\nВсего заказов в списке: {len(offers_list)}")

            found_order = None
            for offer in offers_list:
                if offer.number == created_offer_number:
                    found_order = offer
                    break

            assert found_order is not None, \
                f"Созданный заказ {created_offer_number} не найден в CommerceList"

            print(f"\n✓ Заказ {created_offer_number} найден в CommerceList!")
            print(f"  - ID: {found_order.id}")
            print(f"  - Статус: {found_order.status.value}")
            print(f"  - Сумма: {found_order.total_offer_amount.value} {found_order.total_offer_amount.currency}")

            print("\nТест успешно выполнен!")