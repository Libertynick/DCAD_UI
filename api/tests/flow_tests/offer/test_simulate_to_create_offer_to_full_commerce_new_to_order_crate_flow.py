import allure
import pytest
from datetime import datetime, timedelta

from api_testing_project.services.order.api.api_order_simulate import ApiOrderSimulate
from api_testing_project.services.order.payloads.payloads_order_simulate import PayloadsOrderSimulate
from api_testing_project.services.crm_commerce.create_offer.api.api_create_offer import ApiCreateOffer
from api_testing_project.services.crm_commerce.create_offer.payloads.payloads_create_offer import PayloadsCreateOffer
from api_testing_project.services.crm_commerce.full_commerce_new.api.api_full_commerce_new import FullCommerceNewApi
from api_testing_project.services.order.api.api_order_create import ApiOrderCreate
from api_testing_project.services.order.api.api_order_update_offer import ApiOrderUpdateOffer
from api_testing_project.services.order.payloads.payloads_order_create import PayloadsOrderCreateWithOneCode
from api_testing_project.services.order.payloads.payloads_order_update_offer import PayloadsOrderUpdateOffer
from api_testing_project.utils.offer_flow_helper import OfferFlowHelper


# Конфигурация тестов для разных типов КП (материалов)
"""ВАЖНО при накатке надо поменять поле  'specificationId', берем ео из объекта через дев тулз значение aria-controls"""
true = True
false = False
null = None
TEST_CONFIGS = {
    'Material': {
        'simulate_payload': PayloadsOrderSimulate.order_simulate_add_to_cart_material,
        'delivery_options_key': 'deliveryOptions',
        'line_type': 'Material',
        'quantity_increase': 5,
        'discount_percent': 10,
        'description': 'Material code - full flow with UpdateOffer'
    },

    'BTP': {
        'simulate_payload': PayloadsOrderSimulate.order_simulate_add_to_cart_btp,
        'delivery_options_key': 'deliveryOptionsProd',
        'line_type': 'BTP',
        'quantity_increase': 1,
        'discount_percent': 10,
        'description': 'BTP code - full flow with UpdateOffer',
        'personId': '1c26afd2-1d97-4b7f-92fb-dd21ed412eea',
        'passportId': '4dbb2a44-d895-468d-a51f-ae98b9b3d487',
        'specTypeId': '02061701-51E6-402E-B18F-7BAE7A27F6FB',
        'specificationId': 'bc9bee94-83e3-4402-bbf7-7558069384eb',
        'purchaseType': 'C8EC0EE8-FB5D-4AE1-A664-B2C46A914E46',
        'finalBuyerId': 'daa47b0f-8c66-42f9-a5df-44fae4ff18e8',
        'customerId': 'acb8f425-c3b6-4b38-9f34-1e7fbfd53fa9',
        'exchangeRateType': 'YRU',
        'currencySpecialFixation': True,
        'setContractDiscounts': True,
        'isDraft': True
    },

    'Industrial': {
        'simulate_payload': PayloadsOrderSimulate.order_simulate_add_to_cart_industrial,
        'delivery_options_key': 'deliveryOptionsDZRProd',
        'line_type': 'HEX',
        'quantity_increase': 1,
        'discount_percent': 0,
        'description': 'Industrial HEX code - FROM ORGANIZATION',
        'docType': 'Order',
        'showPriceWithDiscount': False,
        'showDiscount': True,
        'currencyDate': '2025-10-15T00:00:00',
        'currency': 'RUB',
        'exchangeRateType': 'YRU',
        'userName': 'RUCO1845',
        'personId': 'b898f86a-6070-451b-9a14-47ba949c8cb8',
        'usePromoCurrency': False,
        #'opportunityId': 'CF0F3885-3CA5-409D-A270-5E82E6EFD02C',
        'paymentTerms': 'RU00',
        'surchargesPayment': '0',
        'surchargesConversion': 0,
        'payPercentBeforePlacingIntoProduction': 100,
        'isDraft': True,
        'isEndUserPQ': False,
        'purchaseType': '121B015A-E76D-4688-9BB6-2A56EC6DE2EF',
        'finalBuyerId': 'BF2FE82C-FED9-414B-9BA3-403CE76C9000',
        'customerId': 'BF2FE82C-FED9-414B-9BA3-403CE76C9000',
        'clientInn': '5249173547',
        'autoAvailableForDistributor': None,
        'debtorAccount': '31/25-CH',
        'currencySpecialFixation': True,
        'setContractDiscounts': True,
        'isExport': False,
        'validDays': 3,
        'source': None,
        'sellerId': '20C340FE-6AFF-486F-B248-FD8DBE2C93CD',
        'IsATOffer': False,
        'autoFromEngSpec': False,
        'isNew': True,
        'extendedWarranty': {'type': '0'},
        'priceFixingCorridorValue': None,
        'isEstimateOffer': False,
        'offerType': None,
        'passportId': '4DBB2A44-D895-468D-A51F-AE98B9B3D487',
        'specTypeId': '346A197D-F0D1-46E1-9922-C5386D05E3B6',
        'specificationId': 'bc9bee94-83e3-4402-bbf7-7558069384eb',
    },

    'HR': {
        'simulate_payload': PayloadsOrderSimulate.order_simulate_add_to_cart_radiator,
        'delivery_options_key': 'deliveryOptions',
        'line_type': 'Material',
        'quantity_increase': 1,
        'discount_percent': 10,
        'description': 'HR Radiator code - full flow with UpdateOffer',
        'personId': '0b9a97d3-821d-4f84-b016-d3ab2b433bb7',
        'passportId': '9abbcb6b-91ac-4d69-bbee-d0d0f583e18d',
        'specificationId': 'ece5153c-fbbd-4b55-816e-e7dd035364ad',
        'finalBuyerId': '6e9c40d9-59c3-4576-ab38-8b0724fc92fd',
        'salesGroup': 'RU1',
        'salesOffice': 'RU01',
        'isDraft': True
    },
'CleverHit': {
    'simulate_payload': PayloadsOrderSimulate.order_simulate_add_to_cart_clover_hit,
    'delivery_options_key': 'deliveryOptionsDZRProd',
    'line_type': 'HEX',
    'quantity_increase': 1,
    'discount_percent': 55,
    'description': 'Clever Hit HEX code - with promoCurrency and userName',

    # Основные поля
    'docType': 'Order',
    'showPriceWithDiscount': True,
    'showDiscount': False,
    'currencyDate': '2025-11-05T00:00:00',
    'currency': 'RUB',
    'exchangeRateType': 'YRU',
    'userName': 'RIDANCORP\\RUCO3670',
    'personId': 'f8eaae4a-1309-4b24-95e8-3a092dc30067',
    'usePromoCurrency': True,
    'passportId': '4dbb2a44-d895-468d-a51f-ae98b9b3d487',
    'specTypeId': '02061701-51E6-402E-B18F-7BAE7A27F6FB',
    'specificationId': 'bc9bee94-83e3-4402-bbf7-7558069384eb',
    'paymentTerms': 'RU00',
    'surchargesPayment': '0',
    'surchargesConversion': 0,
    'payPercentBeforePlacingIntoProduction': 100,
    'isDraft': True,
    'isEndUserPQ': False,
    'purchaseType': '121B015A-E76D-4688-9BB6-2A56EC6DE2EF',
    'finalBuyerId': 'e55f3bae-ef45-43bd-b2f6-9f0148ca5622',
    'customerId': 'acb8f425-c3b6-4b38-9f34-1e7fbfd53fa9',
    'clientInn': '7705238125',
    'autoAvailableForDistributor': None,
    'debtorAccount': 'RT25-7705238125-HE',
    'currencySpecialFixation': True,
    'setContractDiscounts': True,
    'isExport': False,
    'validDays': 14,
    'source': None,
    'sellerId': '20C340FE-6AFF-486F-B248-FD8DBE2C93CD',
    'IsATOffer': False,
    'autoFromEngSpec': False,
    'isNew': True,
    'extendedWarranty': {'type': '0'},
    'priceFixingCorridorValue': None,
    'isEstimateOffer': False,
    'offerType': None,
    'regionsValidityAT': None,

    # КРИТИЧНО: Полный объект deliveryOptionsDZRProd
    'deliveryOptionsDZRProd_override': {
        "ConsigneeCode": None,
        "Condition": "RU",
        "DeliveryCost": 0,
        "ClientFinalDelivery": None,
        "ConsigneeContacts": None,
        "consigneeAgreementDelivery": {
            "SourceFiasId": "00000000-0000-0000-0000-000000000000",
            "Address": "",
            "PaidDelivery": False,
            "ConditionDescription": "Стандартные договорные условия",
            "INN": "6167138751"
        },
        "CostIncludedInOrder": False,
        "totalDeliveryWeight": 40.85,  # ← Вес из Simulate
        "endPoint": "ToTK",
        "deliveryType": "PickupDZR",
        "consigneeId": "00000000-0000-0000-0000-000000000000",
        "deliverFullSetOnly": False
    }
}
}


@pytest.mark.stage
@pytest.mark.dapi
@allure.feature("DAPI")
@allure.story("Simulate -> CreateOffer -> UpdateOffer -> FullCommerceNew -> Order/Create")
class TestSimulateOfferUpdateOfferFullOrderE2E:
    def setup_method(self):
        self.simulate_api = ApiOrderSimulate()
        self.create_offer_api = ApiCreateOffer()
        self.update_offer_api = ApiOrderUpdateOffer()
        self.full_api = FullCommerceNewApi()
        self.order_create_api = ApiOrderCreate()

    def _execute_steps_1_to_3(self, config, config_key=None):
        """
        Выполняет шаги 1-3 (Simulate -> CreateOffer -> FullCommerceNew).
        Возвращает все данные для дальнейшей работы.

        Args:
            config: Конфигурация теста
            config_key: Ключ типа ('Material', 'BTP', 'Industrial', 'HR') - для специфичной логики
        """
        sim_payload = config['simulate_payload']
        delivery_key = config['delivery_options_key']

        # Шаг 1 — Simulate
        with allure.step("POST /api/Order/Simulate"):
            sim_resp = self.simulate_api.post_order_simulate(sim_payload)
            print("SIMULATE RESPONSE")
            print(sim_resp)

            OfferFlowHelper.verify_simulate_response(sim_resp)

            original_quantity = OfferFlowHelper.extract_original_quantity(sim_resp)
            print(f"Исходное количество из Simulate: {original_quantity}")

            order_lines = OfferFlowHelper.create_order_lines_from_simulate(sim_resp["objects"][0])
            print(f"Order lines from Simulate: {order_lines}")

        # Шаг 2 — CreateOffer (с учетом специфики типа)
        with allure.step("POST /api/CrmCommerce/CreateOffer"):
            if config_key == 'HR':
                # Специальный payload для HR
                offer_payload = dict(PayloadsCreateOffer.create_offer_hr_radiator)
                offer_payload["orderLines"] = order_lines

                now = datetime.now()
                offer_payload["purchaseDate"] = now.isoformat()
                offer_payload["deliveryOptions"]["desiredDeliveryDate"] = (now + timedelta(days=1)).isoformat()
            else:
                # Обычный payload для остальных типов
                offer_payload = dict(PayloadsCreateOffer.base_valid_offer)
                offer_payload["orderLines"] = order_lines
                offer_payload.setdefault("paymentTerms", "RU00")

                OfferFlowHelper.prepare_delivery_options(offer_payload, delivery_key, config)

                exclude_fields = {'simulate_payload', 'delivery_options_key', 'line_type',
                  'quantity_increase', 'discount_percent', 'description', 'isDraft',
                  'deliveryOptionsDZRProd_override'}

                OfferFlowHelper.add_config_fields_to_payload(offer_payload, config, exclude_fields)

            offer_payload['userComment'] = f'ТЕСТ флоу методов {config_key} - CreateOffer'

            print("\n" + "=" * 80)
            print("CREATE OFFER PAYLOAD (что отправляем):")
            print(offer_payload)
            print("=" * 80 + "\n")

            offer_resp = self.create_offer_api.post_create_offer(offer_payload)
            print("CREATE OFFER RESPONSE")
            print(offer_resp)

            saved_offer_payload = offer_payload.copy()

            OfferFlowHelper.verify_create_offer_response(offer_resp)

            offers = offer_resp["objects"][0].get("offers") or []
            assert offers, f"CreateOffer: нет offers в ответе: {offer_resp}"

            offer_id = offers[0]["id"]
            offer_number = offers[0].get("number")
            print(f"Created offer_id: {offer_id}, offer_number: {offer_number}")

        # Шаг 3 — FullCommerceNew
        with allure.step("GET /api/CrmCommerce/FullCommerceNew (до UpdateOffer)"):
            full_resp = self.full_api.get_full_commerce_new_by_request_id(offer_id)
            print("FULL COMMERCE NEW RESPONSE (до UpdateOffer)")
            print(full_resp)

            OfferFlowHelper.verify_full_commerce_response(full_resp)

            full_objects = full_resp.get("objects") or []
            assert full_objects, "FullCommerce: пустой objects"

            full_data = full_resp.get("objects", [{}])[0].get("data") or []
            assert full_data, "FullCommerce: пустой data"

            full_offer = full_data[0]
            assert (
                    full_offer.get("crmCommerceId") == offer_id
                    or (offer_number and full_offer.get("commerceNumber") == offer_number)
            ), f"В FullCommerceNew не нашли оффер id={offer_id}, number={offer_number}"

            order_lines = OfferFlowHelper.update_order_lines_with_odid(order_lines, full_resp)
            print(f"Updated order lines with ODID: {order_lines}")

            # Проверка полей после CreateOffer
            with allure.step("Проверка полей после CreateOffer → FullCommerceNew"):
                # Критичная проверка lineType - в тесте явно, т.к. это баг который мы нашли
                line_type_data = OfferFlowHelper.extract_line_type_data(saved_offer_payload, full_resp)

                with allure.step(f" КРИТИЧНО: lineType должен быть '{line_type_data['expected']}'"):
                    print(f"\n  Ожидаем lineType: '{line_type_data['expected']}'")
                    print(f"  Получили lineType: '{line_type_data['actual']}'")

                    assert line_type_data['actual'] == line_type_data['expected'], \
                        f" КРИТИЧНЫЙ БАГ! lineType изменился с '{line_type_data['expected']}' на '{line_type_data['actual']}'"

                    print(f"  lineType корректен: '{line_type_data['actual']}'")

                # Все остальные стандартные поля - в хелпере (массовая проверка)
                OfferFlowHelper.verify_fields_after_create_offer(saved_offer_payload, full_resp, config)

            # Извлекаем seller_id (для HR)
            details = OfferFlowHelper.extract_details_from_full_commerce(full_resp)
            original_seller_id = None
            original_contractor_name = None
            if details:
                original_seller_id = details[0].get("organization", {}).get("contractorId")
                original_contractor_name = details[0].get("organization", {}).get("contractorName")
                if original_seller_id:
                    print(f"Original Seller ID: {original_seller_id}")
                    print(f"Original Contractor Name: {original_contractor_name}")

        return {
            'original_quantity': original_quantity,
            'order_lines': order_lines,
            'offer_id': offer_id,
            'offer_number': offer_number,
            'full_resp': full_resp,
            'saved_offer_payload': saved_offer_payload,
            'original_seller_id': original_seller_id,
            'original_contractor_name': original_contractor_name
        }

    @pytest.mark.stage
    @pytest.mark.parametrize('config_key', ['Material', 'BTP', 'CleverHit'])
    def test_full_chain_with_update_offer(self, config_key):
        """
        Полный цикл теста с обновлением КП:
        1. Simulate - получаем информацию о материале
        2. CreateOffer - создаем КП
        3. FullCommerceNew (1) - получаем ODID позиций
        4. UpdateOffer - обновляем КП (quantity +1, скидки)
        5. FullCommerceNew (2) - проверяем что изменения применились
        6. Order/Create - создаем заказ из обновленного КП
        """
        config = TEST_CONFIGS[config_key]
        quantity_increase = config['quantity_increase']
        discount_percent = config['discount_percent']
        delivery_key = config['delivery_options_key']

        print(f"\n=== Running test for: {config['description']} ===")

        # Шаги 1-3 (вынесены в отдельный метод)
        data = self._execute_steps_1_to_3(config, config_key)
        original_quantity = data['original_quantity']
        order_lines = data['order_lines']
        offer_id = data['offer_id']
        full_resp = data['full_resp']

        # Шаг 4 — UpdateOffer
        with allure.step("POST /api/Order/UpdateOffer (quantity +1, discounts)"):
            updated_order_lines = OfferFlowHelper.prepare_order_lines_for_update(
                order_lines, quantity_increase, discount_percent
            )

            full_data = full_resp["objects"][0]["data"][0]
            opportunity_id = full_data.get("opportunityId")
            print(f"OpportunityId из FullCommerceNew: {opportunity_id}")

            update_payload = dict(PayloadsOrderUpdateOffer.base_update_offer)
            update_payload["offerId"] = offer_id
            update_payload["opportunityId"] = opportunity_id
            update_payload["orderLines"] = updated_order_lines
            update_payload.setdefault("paymentTerms", "RU00")

            OfferFlowHelper.prepare_delivery_options(update_payload, delivery_key, config)

            exclude_fields = {'simulate_payload', 'delivery_options_key', 'line_type',
                              'quantity_increase', 'discount_percent', 'description', 'isDraft'}

            OfferFlowHelper.add_config_fields_to_payload(update_payload, config, exclude_fields)
            update_payload['userComment'] = 'ТЕСТ флоу методов - UpdateOffer'

            print("\n" + "=" * 80)
            print("UPDATE OFFER PAYLOAD (что отправляем):")
            print(update_payload)
            print("=" * 80 + "\n")

            update_resp = self.update_offer_api.post_update_offer(update_payload)
            print("UPDATE OFFER RESPONSE")
            print(update_resp)

            OfferFlowHelper.verify_update_offer_response(update_resp)
            print("✓ UpdateOffer успешно выполнен!")

        # Шаг 5 — FullCommerceNew (второй раз - проверяем изменения)
        with allure.step("GET /api/CrmCommerce/FullCommerceNew (после UpdateOffer)"):
            full_resp_after = self.full_api.get_full_commerce_new_by_request_id(offer_id)
            print("FULL COMMERCE NEW RESPONSE (после UpdateOffer)")
            print(full_resp_after)

            OfferFlowHelper.verify_full_commerce_response(full_resp_after)

            details = OfferFlowHelper.extract_details_from_full_commerce(full_resp_after)
            assert details, "FullCommerce: нет details после UpdateOffer"

            OfferFlowHelper.verify_quantity_update(details, original_quantity, quantity_increase)
            OfferFlowHelper.verify_discount_update(details, discount_percent)

            # Проверка всех полей
            with allure.step("Проверка всех полей после UpdateOffer → FullCommerceNew"):
                OfferFlowHelper.verify_fields_after_update_offer(
                    update_payload=update_payload,
                    full_response=full_resp_after,
                    config=config,
                    original_quantity=original_quantity,
                    quantity_increase=quantity_increase,
                    discount_percent=discount_percent
                )

            print(f"✓ Все изменения успешно применились!")

            order_lines_for_create = OfferFlowHelper.update_order_lines_with_odid(updated_order_lines, full_resp_after)

        # Шаг 6 — Order/Create
        with allure.step("POST /api/Order/Create"):
            order_payload = dict(
                PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_materials_prepayment_pickup)
            order_payload["orderLines"] = order_lines_for_create
            order_payload["offerId"] = offer_id
            OfferFlowHelper.prepare_delivery_options(order_payload, delivery_key, config)
            order_payload.setdefault("paymentTerms", "RU00")
            order_payload['userComment'] = 'ТЕСТ флоу методов - Order/Create'

            print("ORDER CREATE PAYLOAD")
            print(order_payload)

            order_resp = self.order_create_api.post_order_create(order_payload)
            print("ORDER CREATE RESPONSE")
            print(order_resp)

            OfferFlowHelper.verify_order_create_response(order_resp)

            print("Тест успешно выполнен! Весь цикл с UpdateOffer завершен.")

    @pytest.mark.stage
    @pytest.mark.parametrize('config_key', ['Industrial', 'HR'])
    def test_industrial_chain_without_order(self, config_key):
        """
        Флоу для Industrial (HEX) и Radiator (HR) БЕЗ создания заказа:
        1. Simulate - получаем информацию о материале
        2. CreateOffer - создаем КП (isDraft=True)
        3. FullCommerceNew (1) - получаем ODID позиций
        4. UpdateOffer - обновляем КП (quantity +1, скидки, isDraft=False)
        5. FullCommerceNew (2) - проверяем что изменения применились

        ВАЖНО: Order/Create НЕ делаем, т.к. КП остается в статусе "Согласование"
        """
        config = TEST_CONFIGS[config_key]
        quantity_increase = config['quantity_increase']
        discount_percent = config['discount_percent']
        delivery_key = config['delivery_options_key']

        print(f"\n=== Running test for: {config['description']} ===")

        # Шаги 1-3 (используем универсальный метод!)
        data = self._execute_steps_1_to_3(config, config_key)
        original_quantity = data['original_quantity']
        order_lines = data['order_lines']
        offer_id = data['offer_id']
        full_resp = data['full_resp']
        saved_offer_payload = data['saved_offer_payload']
        original_seller_id = data['original_seller_id']
        original_contractor_name = data['original_contractor_name']

        # Шаг 4 — UpdateOffer
        with allure.step("POST /api/Order/UpdateOffer (quantity +1, discounts, isDraft → False)"):
            updated_order_lines = OfferFlowHelper.prepare_order_lines_for_update(
                order_lines, quantity_increase, discount_percent
            )

            opportunity_id = OfferFlowHelper.extract_opportunity_id(full_resp)
            print(f"OpportunityId из FullCommerceNew: {opportunity_id}")

            if config_key == 'HR':
                update_payload = dict(saved_offer_payload)
                update_payload["offerId"] = offer_id
                update_payload["opportunityId"] = opportunity_id
                update_payload["orderLines"] = updated_order_lines
                update_payload["isDraft"] = False
                update_payload["userComment"] = "ТЕСТ флоу методов HR - UpdateOffer"

                if original_seller_id:
                    update_payload["sellerId"] = original_seller_id
                    print(f"Добавили sellerId в UpdateOffer: {original_seller_id}")
            else:
                update_payload = dict(PayloadsOrderUpdateOffer.base_update_offer)
                update_payload["offerId"] = offer_id
                update_payload["opportunityId"] = opportunity_id
                update_payload["orderLines"] = updated_order_lines
                update_payload.setdefault("paymentTerms", "RU00")
                OfferFlowHelper.prepare_delivery_options(update_payload, delivery_key, config)
                exclude_fields = {'simulate_payload', 'delivery_options_key', 'line_type',
                                  'quantity_increase', 'discount_percent', 'description', 'isDraft', 'isNew'}
                OfferFlowHelper.add_config_fields_to_payload(update_payload, config, exclude_fields)
                update_payload['userComment'] = 'ТЕСТ флоу методов Industrial - UpdateOffer'

            print("\n" + "=" * 80)
            print("UPDATE OFFER PAYLOAD (что отправляем):")
            print(update_payload)
            print("=" * 80 + "\n")

            update_resp = self.update_offer_api.post_update_offer(update_payload)
            print("UPDATE OFFER RESPONSE")
            print(update_resp)

            OfferFlowHelper.verify_update_offer_response(update_resp)
            print("✓ UpdateOffer успешно выполнен!")

        # Шаг 5 — FullCommerceNew (проверяем изменения)
        with allure.step("GET /api/CrmCommerce/FullCommerceNew (после UpdateOffer)"):
            full_resp_after = self.full_api.get_full_commerce_new_by_request_id(offer_id)
            print("FULL COMMERCE NEW RESPONSE (после UpdateOffer)")
            print(full_resp_after)

            OfferFlowHelper.verify_full_commerce_response(full_resp_after)

            details = OfferFlowHelper.extract_details_from_full_commerce(full_resp_after)
            assert details, "FullCommerce: нет details после UpdateOffer"

            OfferFlowHelper.verify_quantity_update(details, original_quantity, quantity_increase)
            OfferFlowHelper.verify_discount_update(details, discount_percent)

            # Проверка всех полей
            with allure.step("Проверка всех полей после UpdateOffer → FullCommerceNew"):
                OfferFlowHelper.verify_fields_after_update_offer(
                    update_payload=update_payload,
                    full_response=full_resp_after,
                    config=config,
                    original_quantity=original_quantity,
                    quantity_increase=quantity_increase,
                    discount_percent=discount_percent
                )

            # Проверка seller_id для HR
            if config_key == 'HR' and original_seller_id:
                current_seller_id = details[0].get("organization", {}).get("contractorId")
                current_contractor_name = details[0].get("organization", {}).get("contractorName")
                print(f"Продавец после UpdateOffer: {current_contractor_name} ({current_seller_id})")

                assert current_seller_id == original_seller_id, \
                    f"Продавец изменился! Было: {original_contractor_name} ({original_seller_id}), " \
                    f"Стало: {current_contractor_name} ({current_seller_id})"

                print(f"✓ Продавец остался прежним: {current_contractor_name}")

            print(f"✓ Все изменения успешно применились!")

            status_display = full_resp_after["objects"][0]["data"][0].get("statusDisplay")
            print(f"\nСтатус КП после UpdateOffer: {status_display}")
            print("Order/Create НЕ выполняется - КП остается в статусе согласования")

            print("\nТест успешно выполнен! (без Order/Create)")