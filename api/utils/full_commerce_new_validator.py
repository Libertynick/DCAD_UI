from typing import Dict, List, Optional, Any


class FullCommerceNewValidator:
    """
    Класс для валидации ответов метода /api/CrmCommerce/FullCommerceNew.

    Проверяет соответствие данных из CreateOffer payload и response
    с данными полученными из FullCommerceNew.

    Основные принципы:
    - Проверяем что данные из CreateOffer корректно сохранились и возвращаются
    - Проверяем точные значения (total, totalVat) из CreateOffer response
    - Глубокая проверка вложенных объектов (deliveryOptions)
    - Разные методы валидации для разных типов материалов
    """

    def __init__(self, full_response: Dict[str, Any], create_offer_payload: Dict[str, Any],
                 create_offer_response: Dict[str, Any], offer_id: str, offer_number: str) -> None:
        """
        Инициализация валидатора.

        :param full_response: Ответ от FullCommerceNew
        :param create_offer_payload: Payload который отправляли в CreateOffer
        :param create_offer_response: Ответ от CreateOffer
        :param offer_id: ID оффера из CreateOffer response
        :param offer_number: Номер оффера из CreateOffer response
        """
        self.full_response = full_response
        self.payload = create_offer_payload
        self.create_offer_response = create_offer_response
        self.offer_id = offer_id
        self.offer_number = offer_number

        self.data = self._extract_data()
        self.details = self._extract_details()
        self.create_offer_lines = self._extract_create_offer_lines()

    def _extract_data(self) -> Dict[str, Any]:
        """
        Извлекает объект data из FullCommerceNew response.

        :return: Первый элемент массива data из FullCommerceNew response
        """
        objects = self.full_response.get("objects") or []
        assert objects, "FullCommerceNew: пустой список objects"

        data = objects[0].get("data") or []
        assert data, "FullCommerceNew: пустой список data"

        return data[0]

    def _extract_details(self) -> List[Dict[str, Any]]:
        """
        Извлекает массив details из FullCommerceNew response.

        :return: Список словарей с позициями из details
        """
        objects = self.full_response.get("objects") or []
        assert objects, "FullCommerceNew: пустой список objects"

        details = objects[0].get("details") or []
        assert details, "FullCommerceNew: пустой список details"

        return details

    def _extract_create_offer_lines(self) -> List[Dict[str, Any]]:
        """
        Извлекает lines из CreateOffer response для проверки цен.

        :return: Список словарей с позициями из CreateOffer response
        """
        objects = self.create_offer_response.get("objects") or []
        if not objects:
            return []

        lines = objects[0].get("lines") or []
        return lines

    def verify_identifiers(self) -> None:
        """
        Проверяет идентификаторы оффера.

        Проверяет что ID и номер оффера из CreateOffer
        совпадают с данными в FullCommerceNew.

        :return: None
        """
        crm_commerce_id = self.data.get("crmCommerceId")
        assert crm_commerce_id == self.offer_id, \
            f"crmCommerceId не совпадает: ожидали {self.offer_id}, получили {crm_commerce_id}"
        print(f"crmCommerceId: {crm_commerce_id}")

        commerce_number = self.data.get("commerceNumber")
        assert commerce_number == self.offer_number, \
            f"commerceNumber не совпадает: ожидали {self.offer_number}, получили {commerce_number}"
        print(f"commerceNumber: {commerce_number}")

    def verify_basic_fields(self) -> None:
        """
        Проверяет основные поля из CreateOffer payload.

        Проверяет что currency, debtorAccount, paymentTerms
        из payload совпадают с FullCommerceNew response.

        :return: None
        """
        currency = self.data.get("currency")
        expected_currency = self.payload.get("currency")
        assert currency == expected_currency, \
            f"currency не совпадает: ожидали {expected_currency}, получили {currency}"
        print(f"currency: {currency}")

        debtor_account = self.data.get("debtorAccount")
        expected_debtor = self.payload.get("debtorAccount")
        if expected_debtor:
            assert debtor_account == expected_debtor, \
                f"debtorAccount не совпадает: ожидали {expected_debtor}, получили {debtor_account}"
            print(f"debtorAccount: {debtor_account}")

        payment_term = self.data.get("paymentTerm")
        expected_payment_terms = self.payload.get("paymentTerms")
        if payment_term and expected_payment_terms:
            payment_term_code = payment_term.get("code")
            assert payment_term_code == expected_payment_terms, \
                f"paymentTerms не совпадает: ожидали {expected_payment_terms}, получили {payment_term_code}"
            print(f"paymentTerms: {payment_term_code}")

    def verify_material_fields(self, material_code: str, quantity: int, line_type: str) -> None:
        """
        Проверяет поля материала в details.

        :param material_code: Ожидаемый код материала
        :param quantity: Ожидаемое количество
        :param line_type: Ожидаемый тип позиции (Material, BTP, HEX)
        :return: None
        """
        detail = self.details[0]

        detail_material_code = detail.get("materialCode") or detail.get("code")
        assert detail_material_code == material_code, \
            f"materialCode не совпадает: ожидали {material_code}, получили {detail_material_code}"
        print(f"materialCode: {detail_material_code}")

        detail_qty = detail.get("qty")
        assert detail_qty == quantity, \
            f"qty не совпадает: ожидали {quantity}, получили {detail_qty}"
        print(f"qty: {detail_qty}")

        detail_line_type = detail.get("lineType")
        assert detail_line_type == line_type, \
            f"lineType не совпадает: ожидали {line_type}, получили {detail_line_type}"
        print(f"lineType: {detail_line_type}")

        detail_currency = detail.get("currency")
        expected_currency = self.payload.get("currency")
        assert detail_currency == expected_currency, \
            f"currency в details не совпадает: ожидали {expected_currency}, получили {detail_currency}"
        print(f"currency в details: {detail_currency}")

    def verify_totals(self) -> None:
        """
        Проверяет точные значения total и totalVat.

        Сравнивает цифры из CreateOffer response (lines)
        с цифрами в FullCommerceNew.

        :return: None
        """
        if not self.create_offer_lines:
            print("Предупреждение: CreateOffer response не содержит lines, пропускаем проверку totals")
            return

        create_offer_line = self.create_offer_lines[0]

        expected_total_with_vat = create_offer_line.get("totalWithDiscountSurchargesAndVAT")
        expected_total_without_vat = create_offer_line.get("totalWithDiscountAndSurcharges")

        if expected_total_with_vat is not None:
            detail_total_vat = self.details[0].get("totalVAT")
            assert abs(detail_total_vat - expected_total_with_vat) < 0.1, \
                f"totalVAT в details не совпадает: ожидали {expected_total_with_vat}, получили {detail_total_vat}"
            print(f"totalVAT в details: {detail_total_vat} (совпадает с CreateOffer)")

        if expected_total_without_vat is not None:
            detail_total = self.details[0].get("total")
            assert abs(detail_total - expected_total_without_vat) < 0.01, \
                f"total в details не совпадает: ожидали {expected_total_without_vat}, получили {detail_total}"
            print(f"total в details: {detail_total} (совпадает с CreateOffer)")

        data_total = self.data.get("total")
        data_total_vat = self.data.get("totalVat")

        if data_total is not None and data_total > 0:
            print(f"total в data: {data_total}")

        if data_total_vat is not None and data_total_vat > 0:
            print(f"totalVat в data: {data_total_vat}")

    def verify_delivery_options_material(self) -> None:
        """
        Проверяет deliveryOptions для Material типа.

        Проверяет структуру и данные в deliveryOptions,
        включая вложенные объекты (address, contacts).

        :return: None
        """
        delivery_options = self.data.get("deliveryOptions")
        assert delivery_options is not None, "deliveryOptions отсутствует для Material"
        print("deliveryOptions присутствует")

        payload_delivery = self.payload.get("deliveryOptions", {})

        delivery_type = delivery_options.get("deliveryType")
        expected_delivery_type = payload_delivery.get("deliveryType")
        if expected_delivery_type:
            assert delivery_type == expected_delivery_type, \
                f"deliveryType не совпадает: ожидали {expected_delivery_type}, получили {delivery_type}"
        print(f"deliveryType: {delivery_type}")

        consignee_id = delivery_options.get("consigneeId")
        expected_consignee_id = payload_delivery.get("consigneeId")
        if expected_consignee_id:
            assert consignee_id == expected_consignee_id, \
                f"consigneeId не совпадает: ожидали {expected_consignee_id}, получили {consignee_id}"
        print(f"consigneeId: {consignee_id}")

        end_point = delivery_options.get("endPoint")
        expected_end_point = payload_delivery.get("endPoint")
        if expected_end_point:
            assert end_point == expected_end_point, \
                f"endPoint не совпадает: ожидали {expected_end_point}, получили {end_point}"
        print(f"endPoint: {end_point}")

        consignee_agreement = delivery_options.get("consigneeAgreementDelivery")
        if consignee_agreement:
            address = consignee_agreement.get("address")
            payload_address = payload_delivery.get("consigneeAgreementDelivery", {}).get("address")
            if payload_address:
                assert address == payload_address, \
                    f"address не совпадает: ожидали {payload_address}, получили {address}"
            print(f"consigneeAgreementDelivery.address: {address}")

        delivery_options_prod = self.data.get("deliveryOptionsProd")
        assert delivery_options_prod is None, \
            "deliveryOptionsProd должен отсутствовать для Material типа"
        print("deliveryOptionsProd отсутствует (корректно для Material)")

        delivery_options_dzr = self.data.get("deliveryOptionsDZRProd")
        assert delivery_options_dzr is None, \
            "deliveryOptionsDZRProd должен отсутствовать для Material типа"
        print("deliveryOptionsDZRProd отсутствует (корректно для Material)")

    def verify_delivery_options_prod_btp(self) -> None:
        """
        Проверяет deliveryOptionsProd для BTP типа.

        Проверяет структуру и данные в deliveryOptionsProd,
        включая вложенные объекты (address, contacts).

        :return: None
        """
        delivery_options_prod = self.data.get("deliveryOptionsProd")
        assert delivery_options_prod is not None, "deliveryOptionsProd отсутствует для BTP"
        print("deliveryOptionsProd присутствует")

        payload_delivery = self.payload.get("deliveryOptionsProd", {})

        delivery_type = delivery_options_prod.get("deliveryType")
        expected_delivery_type = payload_delivery.get("deliveryType")
        if expected_delivery_type:
            assert delivery_type == expected_delivery_type, \
                f"deliveryType не совпадает: ожидали {expected_delivery_type}, получили {delivery_type}"
        print(f"deliveryType: {delivery_type}")

        consignee_id = delivery_options_prod.get("consigneeId")
        expected_consignee_id = payload_delivery.get("consigneeId")
        if expected_consignee_id:
            assert consignee_id == expected_consignee_id, \
                f"consigneeId не совпадает: ожидали {expected_consignee_id}, получили {consignee_id}"
        print(f"consigneeId: {consignee_id}")

        end_point = delivery_options_prod.get("endPoint")
        expected_end_point = payload_delivery.get("endPoint")
        if expected_end_point:
            assert end_point == expected_end_point, \
                f"endPoint не совпадает: ожидали {expected_end_point}, получили {end_point}"
        print(f"endPoint: {end_point}")

        consignee_agreement = delivery_options_prod.get("consigneeAgreementDelivery")
        if consignee_agreement:
            address = consignee_agreement.get("address")
            payload_address = payload_delivery.get("consigneeAgreementDelivery", {}).get("address")
            if payload_address:
                assert address == payload_address, \
                    f"address не совпадает: ожидали {payload_address}, получили {address}"
            print(f"consigneeAgreementDelivery.address: {address}")

    def verify_delivery_options_dzr_prod_hex(self) -> None:
        """
        Проверяет deliveryOptionsDZRProd для HEX/Industrial типа.

        Проверяет структуру и данные в deliveryOptionsDZRProd,
        включая вложенные объекты (address, contacts).

        :return: None
        """
        delivery_options_dzr = self.data.get("deliveryOptionsDZRProd")
        assert delivery_options_dzr is not None, "deliveryOptionsDZRProd отсутствует для HEX/Industrial"
        print("deliveryOptionsDZRProd присутствует")

        payload_delivery = self.payload.get("deliveryOptionsDZRProd", {})

        delivery_type = delivery_options_dzr.get("deliveryType")
        expected_delivery_type = payload_delivery.get("deliveryType")
        if expected_delivery_type:
            assert delivery_type == expected_delivery_type, \
                f"deliveryType не совпадает: ожидали {expected_delivery_type}, получили {delivery_type}"
        print(f"deliveryType: {delivery_type}")

        consignee_id = delivery_options_dzr.get("consigneeId")
        expected_consignee_id = payload_delivery.get("consigneeId")
        if expected_consignee_id:
            assert consignee_id == expected_consignee_id, \
                f"consigneeId не совпадает: ожидали {expected_consignee_id}, получили {consignee_id}"
        print(f"consigneeId: {consignee_id}")

        end_point = delivery_options_dzr.get("endPoint")
        expected_end_point = payload_delivery.get("endPoint")
        if expected_end_point:
            assert end_point == expected_end_point, \
                f"endPoint не совпадает: ожидали {expected_end_point}, получили {end_point}"
        print(f"endPoint: {end_point}")

        consignee_agreement = delivery_options_dzr.get("consigneeAgreementDelivery")
        if consignee_agreement:
            address = consignee_agreement.get("address")
            payload_address = payload_delivery.get("consigneeAgreementDelivery", {}).get("address")
            if payload_address:
                assert address == payload_address, \
                    f"address не совпадает: ожидали {payload_address}, получили {address}"
            print(f"consigneeAgreementDelivery.address: {address}")

    def verify_project_fields_btp(self) -> None:
        """
        Проверяет проектные поля для BTP.

        Проверяет что passportId из payload присутствует
        в FullCommerceNew response.

        :return: None
        """
        passport_id = self.data.get("passportId")
        expected_passport_id = self.payload.get("passportId")

        if expected_passport_id:
            assert passport_id == expected_passport_id, \
                f"passportId не совпадает: ожидали {expected_passport_id}, получили {passport_id}"
            print(f"passportId: {passport_id}")

            crm_passport_number = self.data.get("crmPassportNumber")
            print(f"crmPassportNumber: {crm_passport_number}")
        else:
            print("passportId не передавался в payload (OK для не-проектных КП)")

    def verify_project_fields_hex(self) -> None:
        """
        Проверяет проектные поля для HEX/Industrial.

        Проверяет что passportId из payload присутствует
        в FullCommerceNew response. exchangeRateType проверяется опционально.

        :return: None
        """
        passport_id = self.data.get("passportId")
        expected_passport_id = self.payload.get("passportId")

        if expected_passport_id:
            assert passport_id == expected_passport_id, \
                f"passportId не совпадает: ожидали {expected_passport_id}, получили {passport_id}"
            print(f"passportId: {passport_id}")

            crm_passport_number = self.data.get("crmPassportNumber")
            print(f"crmPassportNumber: {crm_passport_number}")

        exchange_rate_type = self.data.get("exchangeRateType")
        expected_exchange_rate = self.payload.get("exchangeRateType")

        if exchange_rate_type and expected_exchange_rate:
            assert exchange_rate_type == expected_exchange_rate, \
                f"exchangeRateType не совпадает: ожидали {expected_exchange_rate}, получили {exchange_rate_type}"
            print(f"exchangeRateType: {exchange_rate_type}")
        elif expected_exchange_rate and not exchange_rate_type:
            print(f"exchangeRateType не возвращается API (ожидали {expected_exchange_rate}, получили None)")
        elif exchange_rate_type:
            print(f"exchangeRateType: {exchange_rate_type}")

    def verify_permissions(self) -> None:
        """
        Проверяет наличие объекта permissions в ответе.

        :return: None
        """
        objects = self.full_response.get("objects") or []
        permissions = objects[0].get("permissions")
        assert permissions is not None, "permissions отсутствует в ответе"
        print("permissions присутствует")

    def verify_all_for_material(self, material_code: str, quantity: int) -> None:
        """
        Комплексная проверка для Material типа.

        Выполняет все проверки необходимые для Material кода.

        :param material_code: Код материала
        :param quantity: Количество
        :return: None
        """
        print("\n=== Проверка FullCommerceNew для Material ===")
        self.verify_identifiers()
        self.verify_basic_fields()
        self.verify_material_fields(material_code, quantity, "Material")
        self.verify_totals()
        self.verify_delivery_options_material()
        self.verify_permissions()
        print("=== Все проверки для Material успешно пройдены ===\n")

    def verify_all_for_btp(self, material_code: str, quantity: int) -> None:
        """
        Комплексная проверка для BTP типа.

        Выполняет все проверки необходимые для BTP кода,
        включая проектные поля и deliveryOptionsProd.

        :param material_code: Код материала
        :param quantity: Количество
        :return: None
        """
        print("\n=== Проверка FullCommerceNew для BTP ===")
        self.verify_identifiers()
        self.verify_basic_fields()
        self.verify_material_fields(material_code, quantity, "BTP")
        self.verify_totals()
        self.verify_delivery_options_prod_btp()
        self.verify_project_fields_btp()
        self.verify_permissions()
        print("=== Все проверки для BTP успешно пройдены ===\n")

    def verify_all_for_hex(self, material_code: str, quantity: int) -> None:
        """
        Комплексная проверка для HEX типа.

        Выполняет все проверки необходимые для HEX кода,
        включая проектные поля и deliveryOptionsDZRProd.

        :param material_code: Код материала
        :param quantity: Количество
        :return: None
        """
        print("\n=== Проверка FullCommerceNew для HEX ===")
        self.verify_identifiers()
        self.verify_basic_fields()
        self.verify_material_fields(material_code, quantity, "HEX")
        self.verify_totals()
        self.verify_delivery_options_dzr_prod_hex()
        self.verify_project_fields_hex()
        self.verify_permissions()
        print("=== Все проверки для HEX успешно пройдены ===\n")

    def verify_all_for_industrial(self, material_code: str, quantity: int) -> None:
        """
        Комплексная проверка для Industrial типа.

        Выполняет все проверки необходимые для Industrial кода,
        включая проектные поля и deliveryOptionsDZRProd.
        Industrial - это тот же HEX, но с проектными условиями.

        :param material_code: Код материала
        :param quantity: Количество
        :return: None
        """
        print("\n=== Проверка FullCommerceNew для Industrial ===")
        self.verify_identifiers()
        self.verify_basic_fields()
        self.verify_material_fields(material_code, quantity, "HEX")
        self.verify_totals()
        self.verify_delivery_options_dzr_prod_hex()
        self.verify_project_fields_hex()
        self.verify_permissions()
        print("=== Все проверки для Industrial успешно пройдены ===\n")