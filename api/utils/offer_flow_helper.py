"""
Helper класс для работы с флоу тестами Offer.
Содержит методы для:
- Парсинга ответов API
- Подготовки payload'ов
- Обновления данных
- Проверок
"""
from typing import Dict, List, Any, Optional
from api_testing_project.services.crm_commerce.create_offer.payloads.payloads_create_offer import PayloadsCreateOffer


class OfferFlowHelper:
    """
    Helper класс для упрощения работы с флоу-тестами на Offer.
    Все методы статические, так как не требуют состояния.
    """

    # ========== ГРУППА 1: ПАРСИНГ ОТВЕТОВ API ==========

    @staticmethod
    def extract_offer_id(create_offer_response: Dict) -> str:
        """Извлекает offer_id из ответа CreateOffer."""
        offers = create_offer_response.get("objects", [{}])[0].get("offers") or []
        assert offers, f"CreateOffer: нет offers в ответе: {create_offer_response}"
        return offers[0]["id"]

    @staticmethod
    def extract_offer_number(create_offer_response: Dict) -> str:
        """Извлекает offer_number из ответа CreateOffer."""
        offers = create_offer_response.get("objects", [{}])[0].get("offers") or []
        return offers[0].get("number") if offers else None

    @staticmethod
    def extract_opportunity_id(full_commerce_response: Dict) -> Optional[str]:
        """Извлекает opportunityId из ответа FullCommerceNew."""
        full_objects = full_commerce_response.get("objects") or []
        if not full_objects:
            return None

        data = full_objects[0].get("data", [])  # ← data это СПИСОК!
        if not data:
            return None

        return data[0].get("opportunityId")  # ← берем первый элемент

    @staticmethod
    def extract_seller_id(full_commerce_response: Dict) -> Optional[str]:
        """Извлекает sellerId из ответа FullCommerceNew. Используется для HR типа."""
        full_objects = full_commerce_response.get("objects") or []
        if not full_objects:
            return None

        data = full_objects[0].get("data", [])  # ← data это СПИСОК!
        if not data:
            return None

        orders = data[0].get("orders") or []  # ← берем первый элемент
        if not orders:
            return None

        return orders[0].get("sellerId")

    @staticmethod
    def extract_original_quantity(simulate_response: Dict) -> int:
        """Извлекает исходное количество из ответа Simulate."""
        return simulate_response["objects"][0]["orderLines"][0].get("orderedQuantity")

    @staticmethod
    def extract_details_from_full_commerce(full_commerce_response: Dict) -> List[Dict]:
        """Извлекает details из ответа FullCommerceNew."""
        full_objects = full_commerce_response.get("objects") or []
        if not full_objects:
            return []
        return full_objects[0].get("details", [])

    # ========== ГРУППА 2: СОЗДАНИЕ ORDER LINES ==========

    @staticmethod
    def create_order_lines_from_simulate(sim_obj: Dict) -> List[Dict]:
        """Создает orderLines из ответа Simulate (без ODID). ODID будет добавлен позже."""
        line = sim_obj["orderLines"][0]
        qty = line.get("orderedQuantity")

        item = {
            "materialCode": line.get("materialCode"),
            "quantity": qty,
            "lineNumber": line.get("lineNumber"),
            "lineType": line.get("lineType"),
            "odid": line.get("odid"),  # пока None, обновим позже
        }

        schedules = line.get("schedules") or []
        if schedules and schedules[0].get("deliveryDate"):
            item["deliveryDate"] = schedules[0]["deliveryDate"]

        return [item]

    @staticmethod
    def update_order_lines_with_odid(order_lines: List[Dict], full_resp: Dict) -> List[Dict]:
        """Обновляет orderLines правильными ODID из ответа FullCommerceNew. Также добавляет contractorId если он есть."""
        full_objects = full_resp.get("objects", [])
        if not full_objects:
            print("Нет objects в ответе FullCommerceNew")
            return order_lines

        details = full_objects[0].get("details", [])
        if not details:
            print("Нет details в ответе FullCommerceNew")
            return order_lines

        print(f"Найдено {len(details)} позиций в details")

        # Создаем маппинг materialCode -> odid и materialCode -> contractorId
        code_to_odid = {}
        code_to_contractor_id = {}
        for detail in details:
            material_code = detail.get("materialCode") or detail.get("code")
            odid = detail.get("id")
            contractor_id = detail.get("organization", {}).get("contractorId")

            if material_code and odid:
                code_to_odid[material_code] = odid
                print(f"Mapping: {material_code} → {odid}")

                if contractor_id:
                    code_to_contractor_id[material_code] = contractor_id
                    print(f"Contractor: {material_code} → {contractor_id}")

        # Обновляем ODID и contractorId в orderLines
        for line in order_lines:
            mat_code = line.get("materialCode")
            if mat_code in code_to_odid:
                line["odid"] = code_to_odid[mat_code]
                print(f"✓ Updated ODID for {mat_code}: {line['odid']}")

                if mat_code in code_to_contractor_id:
                    line["contractorId"] = code_to_contractor_id[mat_code]
                    print(f"✓ Updated contractorId for {mat_code}: {line['contractorId']}")
            else:
                print(f"⚠ No ODID found for {mat_code}")

        return order_lines

    @staticmethod
    def prepare_order_lines_for_update(order_lines: List[Dict], quantity_increase: int, discount_percent: float) -> List[Dict]:
        """Подготавливает orderLines для UpdateOffer: увеличивает quantity, добавляет скидки, сохраняет contractorId."""
        updated_lines = []
        for line in order_lines:
            updated_line = dict(line)
            updated_line["quantity"] = line["quantity"] + quantity_increase
            updated_line["discountPercent"] = discount_percent
            updated_line["endClientDiscountPercent"] = discount_percent

            if "contractorId" in line:
                updated_line["contractorId"] = line["contractorId"]

            updated_lines.append(updated_line)

        return updated_lines

    # ========== ГРУППА 3: ПОДГОТОВКА PAYLOAD'ОВ ==========

    @staticmethod
    def prepare_delivery_options(payload: Dict, delivery_key: str, config: Dict) -> None:
        """Подготовка delivery options в зависимости от типа материала. Метод изменяет payload in-place."""
        if delivery_key == 'deliveryOptionsProd':
            if "deliveryOptions" in payload:
                payload["deliveryOptionsProd"] = payload.pop("deliveryOptions")

        elif delivery_key == 'deliveryOptionsDZRProd':
            if "deliveryOptions" in payload:
                payload.pop("deliveryOptions")
            # Если в конфиге есть свой deliveryOptionsDZRProd - используем его
            if 'deliveryOptionsDZRProd_override' in config:
                payload["deliveryOptionsDZRProd"] = dict(config['deliveryOptionsDZRProd_override'])
            else:
                # Иначе используем стандартный шаблон для Industrial
                payload["deliveryOptionsDZRProd"] = dict(
                    PayloadsCreateOffer.delivery_options_dzr_prod_industrial
                )
            project_obj = dict(PayloadsCreateOffer.project_object_industrial)
            project_obj["id"] = config.get('passportId')
            payload["projectObject"] = project_obj

        elif delivery_key == 'deliveryOptions':
            if config.get('passportId'):
                payload["projectObject"] = {
                    "id": config.get('passportId'),
                    "name": "Детский сад на 240 мест в г. Тарко-Сале, мкр.Южный",
                    "address": "Ямало-Ненецкий АО, г Тарко-Сале, мкр Южный",
                    "number": 1178586,
                    "comment": " "
                }

    @staticmethod
    def add_config_fields_to_payload(payload: Dict, config: Dict, exclude_fields: set) -> None:
        """Добавляет специфичные поля из конфига в payload. Метод изменяет payload in-place."""
        for key, value in config.items():
            if key not in exclude_fields:
                payload[key] = value

    # ========== ГРУППА 4: ПРОВЕРКИ ==========

    @staticmethod
    def verify_quantity_update(details: List[Dict], original_quantity: int, quantity_increase: int) -> None:
        """Проверяет что количество обновилось корректно в FullCommerceNew."""
        for detail in details:
            material_code = detail.get("materialCode") or detail.get("code")
            qty = detail.get("qty")
            expected_qty = original_quantity + quantity_increase

            print(f"\nПроверка количества для {material_code}:")
            print(f"  Ожидаем: {expected_qty}")
            print(f"  Получили: {qty}")

            assert qty == expected_qty, \
                f"Количество не обновилось для {material_code}. Ожидали {expected_qty}, получили {qty}"

            print(f"✓ Количество корректно!")

    @staticmethod
    def verify_discount_update(details: List[Dict], discount_percent: float) -> None:
        """Проверяет что скидка обновилась корректно в FullCommerceNew."""
        for detail in details:
            material_code = detail.get("materialCode") or detail.get("code")
            end_client_discount = detail.get("clientDiscountPercent", 0)

            print(f"\nПроверка скидки для {material_code}:")
            print(f"  Ожидаем: {discount_percent}%")
            print(f"  Получили: {end_client_discount}%")

            assert end_client_discount == discount_percent, \
                f"Скидка конечного клиента не обновилась для {material_code}. Ожидали {discount_percent}%, получили {end_client_discount}%"

            print(f"✓ Скидка корректна!")

    @staticmethod
    def verify_simulate_response(simulate_response: Dict) -> None:
        """Проверяет базовую валидность ответа Simulate."""
        assert simulate_response["status"] in ["Ok", "Warning"], \
            f"Simulate status != Ok/Warning: {simulate_response}"
        assert simulate_response["objects"], "Simulate: пустой objects"
        assert simulate_response["objects"][0].get("orderLines"), "Simulate: нет orderLines"

    @staticmethod
    def verify_create_offer_response(create_offer_response: Dict) -> None:
        """Проверяет базовую валидность ответа CreateOffer."""
        assert create_offer_response["status"] == "Ok", \
            f"CreateOffer status != Ok: {create_offer_response}"
        assert create_offer_response.get("objects"), "CreateOffer: пустой objects"

    @staticmethod
    def verify_full_commerce_response(full_commerce_response: Dict) -> None:
        """Проверяет базовую валидность ответа FullCommerceNew."""
        assert full_commerce_response["status"] == "Ok", \
            f"FullCommerce status != Ok: {full_commerce_response}"

    @staticmethod
    def verify_update_offer_response(update_offer_response: Dict) -> None:
        """Проверяет базовую валидность ответа UpdateOffer."""
        assert update_offer_response["status"] == "Ok" or update_offer_response["status"] == "Warning", \
            f"UpdateOffer status != Ok: {update_offer_response}"

    @staticmethod
    def verify_order_create_response(order_create_response: Dict) -> None:
        """Проверяет базовую валидность ответа Order/Create."""
        assert order_create_response["status"] == "Ok", \
            f"Order/Create status != Ok: {order_create_response}"
        assert order_create_response.get("objects"), "Order/Create: пустой objects"

    @staticmethod
    def verify_fields_after_create_offer(create_payload: Dict, full_response: Dict, config: Dict) -> None:
        """
        Проверяет стандартные поля после CreateOffer → FullCommerceNew.
        Проверяет: materialCode, quantity, currency, debtorAccount, personId, INN, weight.
        НЕ проверяет lineType - это критичное поле, проверяется в тесте отдельно!
        """
        print("\n" + "=" * 80)
        print("ПРОВЕРКА СТАНДАРТНЫХ ПОЛЕЙ ПОСЛЕ CreateOffer → FullCommerceNew")
        print("=" * 80)

        full_data = full_response.get("objects", [{}])[0].get("data", [{}])[0]
        details_list = full_response.get("objects", [{}])[0].get("details", [])
        details = details_list[0] if details_list else {}
        delivery_dzr = full_data.get("deliveryOptionsDZRProd", {})

        # Проверка materialCode
        expected_material = create_payload["orderLines"][0].get("materialCode")
        actual_material = details.get("code") or details.get("materialCode")
        print(f"\n materialCode: ожидаем '{expected_material}', получили '{actual_material}'")
        assert actual_material == expected_material, \
            f"materialCode не совпадает! Ожидали '{expected_material}', получили '{actual_material}'"

        # Проверка quantity
        expected_qty = create_payload["orderLines"][0].get("quantity")
        actual_qty = details.get("qty")
        print(f" quantity: ожидаем {expected_qty}, получили {actual_qty}")
        assert actual_qty == expected_qty, \
            f"quantity не совпадает! Ожидали {expected_qty}, получили {actual_qty}"

        # Проверка currency
        expected_currency = create_payload.get("currency")
        actual_currency = full_data.get("currency")
        print(f" currency: ожидаем '{expected_currency}', получили '{actual_currency}'")
        assert actual_currency == expected_currency, \
            f"currency не совпадает! Ожидали '{expected_currency}', получили '{actual_currency}'"

        # Проверка debtorAccount
        expected_debtor = create_payload.get("debtorAccount")
        actual_debtor = full_data.get("debtorAccount")
        print(f" debtorAccount: ожидаем '{expected_debtor}', получили '{actual_debtor}'")
        assert actual_debtor == expected_debtor, \
            f"debtorAccount не совпадает! Ожидали '{expected_debtor}', получили '{actual_debtor}'"

        # Проверка personId
        expected_person = create_payload.get("personId")
        actual_person = full_data.get("creatorPersonId")
        print(f" personId: ожидаем '{expected_person}', получили '{actual_person}'")
        assert actual_person == expected_person, \
            f"personId не совпадает! Ожидали '{expected_person}', получили '{actual_person}'"

        # Проверка INN и веса (если есть deliveryOptionsDZRProd_override)
        if "deliveryOptionsDZRProd_override" in config and delivery_dzr:
            expected_inn = config["deliveryOptionsDZRProd_override"]["consigneeAgreementDelivery"]["INN"]
            actual_inn = delivery_dzr.get("consigneeAgreementDelivery", {}).get("inn")
            print(f" INN в deliveryOptions: ожидаем '{expected_inn}', получили '{actual_inn}'")
            assert actual_inn == expected_inn, \
                f"INN не совпадает! Ожидали '{expected_inn}', получили '{actual_inn}'"

            expected_weight = config["deliveryOptionsDZRProd_override"]["totalDeliveryWeight"]
            actual_weight = delivery_dzr.get("totalDeliveryWeight")
            print(f" totalDeliveryWeight: ожидаем {expected_weight}, получили {actual_weight}")
            assert actual_weight == expected_weight, \
                f"totalDeliveryWeight не совпадает! Ожидали {expected_weight}, получили {actual_weight}"

        print("\n Все стандартные поля корректны!")
        print("=" * 80 + "\n")

    @staticmethod
    def extract_line_type_data(create_payload: Dict, full_response: Dict) -> Dict:
        """
        Извлекает lineType из CreateOffer и FullCommerceNew для сравнения.
        Возвращает словарь с ожидаемым и фактическим значением.
        ВАЖНО: Не делает assert - это критичное поле, проверяется в тесте отдельно!
        """
        details_list = full_response.get("objects", [{}])[0].get("details", [])
        details = details_list[0] if details_list else {}

        return {
            'expected': create_payload["orderLines"][0].get("lineType"),
            'actual': details.get("lineType")
        }

    @staticmethod
    def verify_fields_after_update_offer(update_payload: Dict, full_response: Dict, config: Dict,
                                         original_quantity: int, quantity_increase: int,
                                         discount_percent: float) -> None:
        """Проверяет поля после UpdateOffer → FullCommerceNew."""
        print("\n" + "=" * 80)
        print("ПРОВЕРКА ПОЛЕЙ ПОСЛЕ UpdateOffer → FullCommerceNew")
        print("=" * 80)

        full_data = full_response.get("objects", [{}])[0].get("data", [{}])[0]
        details_list = full_response.get("objects", [{}])[0].get("details", [])
        details = details_list[0] if details_list else {}
        delivery_dzr = full_data.get("deliveryOptionsDZRProd", {})

        # materialCode (не меняется)
        expected_material = update_payload["orderLines"][0].get("materialCode")
        actual_material = details.get("code") or details.get("materialCode")
        print(f"\n materialCode: ожидаем '{expected_material}', получили '{actual_material}'")
        assert actual_material == expected_material, \
            f"materialCode не совпадает! Ожидали '{expected_material}', получили '{actual_material}'"

        # quantity (изменился)
        expected_qty = original_quantity + quantity_increase
        actual_qty = details.get("qty")
        print(f" quantity: ожидаем {expected_qty}, получили {actual_qty}")
        assert actual_qty == expected_qty, \
            f"quantity не совпадает! Ожидали {expected_qty}, получили {actual_qty}"

        # discount (изменился)
        actual_discount = details.get("clientDiscountPercent", 0)
        print(f" discount: ожидаем {discount_percent}%, получили {actual_discount}%")
        assert actual_discount == discount_percent, \
            f"discount не совпадает! Ожидали {discount_percent}%, получили {actual_discount}%"

        # currency (не меняется)
        expected_currency = update_payload.get("currency")
        actual_currency = full_data.get("currency")
        print(f" currency: ожидаем '{expected_currency}', получили '{actual_currency}'")
        assert actual_currency == expected_currency, \
            f"currency не совпадает! Ожидали '{expected_currency}', получили '{actual_currency}'"

        # debtorAccount (не меняется)
        expected_debtor = update_payload.get("debtorAccount")
        actual_debtor = full_data.get("debtorAccount")
        print(f" debtorAccount: ожидаем '{expected_debtor}', получили '{actual_debtor}'")
        assert actual_debtor == expected_debtor, \
            f"debtorAccount не совпадает! Ожидали '{expected_debtor}', получили '{actual_debtor}'"

        # personId (не меняется)
        expected_person = update_payload.get("personId")
        if expected_person:
            actual_person = full_data.get("creatorPersonId")
            print(f" personId: ожидаем '{expected_person}', получили '{actual_person}'")
            assert actual_person == expected_person, \
                f"personId не совпадает! Ожидали '{expected_person}', получили '{actual_person}'"

        # lineType (КРИТИЧНО - не меняется!)
        expected_line_type = update_payload["orderLines"][0].get("lineType")
        actual_line_type = details.get("lineType")
        print(f" lineType: ожидаем '{expected_line_type}', получили '{actual_line_type}'")
        assert actual_line_type == expected_line_type, \
            f" БАГ! lineType изменился с '{expected_line_type}' на '{actual_line_type}'"

        # INN и weight (если есть, не меняются)
        if "deliveryOptionsDZRProd_override" in config and delivery_dzr:
            expected_inn = config["deliveryOptionsDZRProd_override"]["consigneeAgreementDelivery"]["INN"]
            actual_inn = delivery_dzr.get("consigneeAgreementDelivery", {}).get("inn")
            print(f" INN: ожидаем '{expected_inn}', получили '{actual_inn}'")
            assert actual_inn == expected_inn, \
                f"INN не совпадает! Ожидали '{expected_inn}', получили '{actual_inn}'"

            expected_weight = config["deliveryOptionsDZRProd_override"]["totalDeliveryWeight"]
            actual_weight = delivery_dzr.get("totalDeliveryWeight")
            print(f" weight: ожидаем {expected_weight}, получили {actual_weight}")
            assert actual_weight == expected_weight, \
                f"weight не совпадает! Ожидали {expected_weight}, получили {actual_weight}"

        print("\n Все поля после UpdateOffer корректны!")
        print("=" * 80 + "\n")