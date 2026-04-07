import allure
import pytest
from dataclasses import dataclass

from api_testing_project.services.crm_commerce.full_commerce_new.api.api_full_commerce_new import FullCommerceNewApi
from api_testing_project.services.order.api.api_order_create import ApiOrderCreate
from api_testing_project.services.order.api.api_order_simulate import ApiOrderSimulate
from api_testing_project.services.order.models.order_create_model import OrderCreateModel
from api_testing_project.services.order.models.order_simulate_model import OrderSimulateModel
from api_testing_project.services.order.payloads.payloads_order_create import PayloadsOrderCreateWithOneCode
from api_testing_project.services.order.payloads.payloads_order_simulate import PayloadsOrderSimulate


class TestCases:
    """Набор тестовых данных"""

    # Набор тестовых данных (simulate and order/create) на предоплату с различными условиями доставки
    test_cases_prepayment = [
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_material,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_materials_prepayment_pickup,
         'id': 'Material. Pickup. Prepayment. request_create_order_with_one_code_materials_prepayment_pickup'
         },
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_pto,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_pto_prepayment_pickup,
         'id': 'PTO. Pickup. Prepayment. request_create_order_with_one_code_pto_prepayment_pickup'
         },
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_pumps,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_pumps_prepayment_pickup,
         'id': 'Pumps. Pickup. Prepayment. request_create_order_with_one_code_pumps_prepayment_pickup'},
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_bom,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_prepayment_pickup_bom,
         'id': 'BOM. Pickup. Prepayment. request_create_order_with_one_code_prepayment_pickup_bom'
         },
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_bast,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_prepayment_pickup_bast,
         'id': 'Bast. Pickup. Prepayment. request_create_order_with_one_code_prepayment_pickup_bast'
         },
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_zip,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_prepayment_pickup_zip,
         'id': 'ZIP. Pickup. Prepayment. request_create_order_with_one_code_prepayment_pickup_zip'
         },
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_tdu,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_prepayment_pickup_tdu,
         'id': 'TDU. Pickup. Prepayment. request_create_order_with_one_code_prepayment_pickup_tdu'
         },
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_material,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_prepayment_delivery_to_address_not_included_to_price_materials,
         'id': 'Material. Delivery to address not included to price. Prepayment. request_create_order_with_one_code_prepayment_delivery_to_address_not_included_to_price_materials'
         },
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_pto,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_prepayment_delivery_to_address_not_included_to_price_pto,
         'id': 'PTO. Delivery to address not included to price. Prepayment. request_create_order_with_one_code_prepayment_delivery_to_address_not_included_to_price_pto'
         },
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_pumps,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_prepayment_delivery_to_address_not_included_to_price_pumps,
         'id': 'Pumps. Delivery to address not included to price. Prepayment. request_create_order_with_one_code_prepayment_delivery_to_address_not_included_to_price_pumps'
         },
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_bom,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_prepayment_delivery_to_address_not_included_to_price_bom,
         'id': 'BOM. Delivery to address not included to price. Prepayment. request_create_order_with_one_code_prepayment_delivery_to_address_not_included_to_price_bom'
         },
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_bast,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_prepayment_delivery_to_address_not_included_to_price_bast,
         'id': 'BAST. Delivery to address not included to price. Prepayment. request_create_order_with_one_code_prepayment_delivery_to_address_not_included_to_price_bast'
         },
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_zip,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_prepayment_delivery_to_address_not_included_to_price_zip,
         'id': 'ZIP. Delivery to address not included to price. Prepayment. request_create_order_with_one_code_prepayment_delivery_to_address_not_included_to_price_zip'
         },
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_tdu,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_prepayment_delivery_to_address_not_included_to_price_tdu,
         'id': 'TDU. Delivery to address not included to price. Prepayment. request_create_order_with_one_code_prepayment_delivery_to_address_not_included_to_price_tdu'
         },
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_material,
         "request_order_create": PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_prepayment_delivery_to_address_included_to_price_materials,
         'id': 'Material. Delivery to address included to price. Prepayment. request_create_order_with_one_code_prepayment_delivery_to_address_included_to_price_materials'
         },
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_pto,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_prepayment_delivery_to_address_included_to_price_pto,
         'id': 'PTO. Delivery to address included to price. Prepayment. request_create_order_with_one_code_prepayment_delivery_to_address_included_to_price_pto'
         },
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_pumps,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_prepayment_delivery_to_address_included_to_price_pumps,
         'id': 'Pumps. Delivery to address included to price. Prepayment. request_create_order_with_one_code_prepayment_delivery_to_address_included_to_price_pumps'
         },
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_bom,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_prepayment_delivery_to_address_included_to_price_bom,
         'id': 'BOM. Delivery to address included to price. Prepayment. request_create_order_with_one_code_prepayment_delivery_to_address_included_to_price_bom'
         },
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_bast,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_prepayment_delivery_to_address_included_to_price_bast,
         'id': 'BAST. Delivery to address included to price. Prepayment. request_create_order_with_one_code_prepayment_delivery_to_address_included_to_price_bast'
         },
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_zip,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_prepayment_delivery_to_address_included_to_price_zip,
         'id': 'ZIP. Delivery to address included to price. Prepayment. request_create_order_with_one_code_prepayment_delivery_to_address_included_to_price_zip'
         },
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_tdu,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_prepayment_delivery_to_address_included_to_price_tdu,
         'id': 'TDU. Delivery to address included to price. Prepayment. request_create_order_with_one_code_prepayment_delivery_to_address_included_to_price_tdu'
         },
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_material,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_prepayment_delivery_to_warehouse_by_agreement_materials,
         'id': 'Material. Delivery to warehouse by agreement. request_create_order_with_one_code_prepayment_delivery_to_warehouse_by_agreement_materials'
         },
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_pto,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_prepayment_delivery_to_warehouse_by_agreement_pto,
         'id': 'PTO. Delivery to warehouse by agreement. request_create_order_with_one_code_prepayment_delivery_to_warehouse_by_agreement_pto'
         },
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_pumps,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_prepayment_delivery_to_warehouse_by_agreement_pumps,
         'id': 'Pumps. Delivery to warehouse by agreement. request_create_order_with_one_code_prepayment_delivery_to_warehouse_by_agreement_pumps'
         },
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_bom,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_prepayment_delivery_to_warehouse_by_agreement_bom,
         'id': 'BOM. Delivery to warehouse by agreement. request_create_order_with_one_code_prepayment_delivery_to_warehouse_by_agreement_bom'
         },
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_bast,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_prepayment_delivery_to_warehouse_by_agreement_bast,
         'id': 'BAST. Delivery to warehouse by agreement. request_create_order_with_one_code_prepayment_delivery_to_warehouse_by_agreement_bast'
         },
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_zip,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_prepayment_delivery_to_warehouse_by_agreement_zip,
         'id': 'ZIP. Delivery to warehouse by agreement. request_create_order_with_one_code_prepayment_delivery_to_warehouse_by_agreement_zip'
         },
        {'request_simulate': PayloadsOrderSimulate.order_simulate_add_to_cart_tdu,
         'request_order_create': PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_prepayment_delivery_to_warehouse_by_agreement_tdu,
         'id': 'TDU. Delivery to warehouse by agreement. request_create_order_with_one_code_prepayment_delivery_to_warehouse_by_agreement_tdu'}
    ]


@dataclass
class ExpectedDataFromOrderCreatePayload:
    """Ожидаемые данные из запроса на order/create"""
    expected_material_code: None
    expected_payment_terms: None
    expected_delivery_condition: None
    expected_delivery_cost: None
    expected_total_delivery_weight: None
    expected_delivery_comment: None
    expected_delivery_end_point: None
    expected_desired_delivery_date: None
    expected_delivery_full_set_only: None
    expected_cost_included_in_order: None
    expected_consignee_id: None
    expected_delivery_type: None
    expected_debtor_account: None
    expected_currency: None
    expected_line_type: None
    line_type_payload: None
    order_type: None


@dataclass
class ExpectedDataFromResponseSimulate:
    """Ожидаемые данные из ответа order/simulate"""
    description_article_in_simulate: None
    discount_distr: float
    sales_price_with_tax: float
    expected_surcharges_percent: float


@pytest.mark.stage
@pytest.mark.dapi
@allure.feature('DAPI')
@allure.story('Тесты на Order/Create')
class TestOrderCreate:
    """Тесты на Order/Create"""
    api_order_simulate = ApiOrderSimulate()
    api_order_create = ApiOrderCreate()

    @staticmethod
    def expected_data_from_payload_order_create(payload_simulate, payload_order_create):
        """Ожидаемые значения из запроса order/create"""
        expected_material_code = payload_simulate["materials"][0]["materialCode"]
        expected_debtor_account = payload_order_create['debtorAccount']
        expected_currency = payload_order_create['currency']
        expected_line_type = payload_order_create['orderLines'][0]['lineType']
        expected_payment_terms = payload_order_create['paymentTerms']
        expected_delivery_condition = None
        expected_delivery_cost = None
        expected_total_delivery_weight = None  # общий вес доставки
        expected_delivery_comment = None
        expected_delivery_end_point = None  # Конечная точная доставки
        expected_desired_delivery_date = None  # Желаемая дата отгрузки
        expected_delivery_full_set_only = None  # Желаемая- Отгружать только при полной комплектации
        expected_cost_included_in_order = None  # Желаемая- Стоимость доставки влючена в заказ (true) или отдельным счетов(false)
        expected_consignee_id = None  # Ожидаемое id грузополучателя
        expected_delivery_type = None

        order_lines_payload = payload_order_create['orderLines'][0]  # Объект order_lines в запросе order/create
        line_type_payload = order_lines_payload['lineType']
        order_type = None  # Тип заказа

        # По типам заказов
        print(order_lines_payload['lineType'], 'lineType')

        if line_type_payload == 'Material':
            order_type = 'Material'

            delivery_option = payload_order_create.get('deliveryOptions')
            try:
                expected_delivery_condition = delivery_option['condition']
            except KeyError:
                expected_delivery_condition = None
            expected_delivery_cost = delivery_option['deliveryCost']
            expected_total_delivery_weight = delivery_option['totalDeliveryWeight']
            expected_delivery_comment = delivery_option['comment']
            expected_delivery_end_point = delivery_option['endPoint']
            expected_desired_delivery_date = delivery_option['desiredDeliveryDate']
            expected_delivery_full_set_only = delivery_option['deliverFullSetOnly']
            expected_cost_included_in_order = delivery_option['costIncludedInOrder']
            expected_consignee_id = delivery_option['consigneeId']
            expected_delivery_type = delivery_option['deliveryType']
        elif line_type_payload == 'HEXAdditions':
            order_type = 'HEXAdditions'

            delivery_option = payload_order_create.get('deliveryOptionsHex')

            expected_delivery_type = delivery_option['deliveryType']
            try:
                expected_delivery_condition = delivery_option['condition']
            except KeyError:
                expected_delivery_condition = None
            expected_delivery_cost = delivery_option['deliveryCost']
            expected_total_delivery_weight = delivery_option['totalDeliveryWeight']
            expected_delivery_comment = delivery_option['comment']
            expected_delivery_end_point = delivery_option['endPoint']
            expected_desired_delivery_date = delivery_option['desiredDeliveryDate']
            expected_delivery_full_set_only = delivery_option['deliverFullSetOnly']
            expected_cost_included_in_order = delivery_option['costIncludedInOrder']
            expected_consignee_id = delivery_option['consigneeId']
        elif line_type_payload in ['HEX', 'Pump']:
            order_type = 'HEX'

            delivery_option = payload_order_create.get('deliveryOptionsDZRProd')

            expected_delivery_type = delivery_option['deliveryType']
            try:
                expected_delivery_condition = delivery_option['condition']
            except KeyError:
                expected_delivery_condition = None
            expected_delivery_cost = delivery_option['deliveryCost']
            expected_total_delivery_weight = delivery_option['totalDeliveryWeight']
            expected_delivery_comment = delivery_option['comment']
            expected_delivery_end_point = delivery_option['endPoint']
            expected_desired_delivery_date = delivery_option['desiredDeliveryDate']
            expected_delivery_full_set_only = delivery_option['deliverFullSetOnly']
            expected_cost_included_in_order = delivery_option['costIncludedInOrder']
            expected_consignee_id = delivery_option['consigneeId']
        elif line_type_payload in ['AutoShield', 'TDU', 'BTP']:
            order_type = 'AutoShield'

            delivery_option = payload_order_create.get('deliveryOptionsProd')

            expected_delivery_type = delivery_option['deliveryType']
            try:
                expected_delivery_condition = delivery_option['condition']
            except KeyError:
                expected_delivery_condition = None
            expected_delivery_cost = delivery_option['deliveryCost']
            expected_total_delivery_weight = delivery_option['totalDeliveryWeight']
            expected_delivery_comment = delivery_option['comment']
            expected_delivery_end_point = delivery_option['endPoint']
            expected_desired_delivery_date = delivery_option['desiredDeliveryDate']
            expected_delivery_full_set_only = delivery_option['deliverFullSetOnly']
            expected_cost_included_in_order = delivery_option['costIncludedInOrder']

        return ExpectedDataFromOrderCreatePayload(
            expected_material_code,
            expected_payment_terms,
            expected_delivery_condition,
            expected_delivery_cost,
            expected_total_delivery_weight,
            expected_delivery_comment,
            expected_delivery_end_point,
            expected_desired_delivery_date,
            expected_delivery_full_set_only,
            expected_cost_included_in_order,
            expected_consignee_id,
            expected_delivery_type,
            expected_debtor_account,
            expected_currency,
            expected_line_type,
            line_type_payload,
            order_type
        )

    def expected_data_from_response_order_simulate(self):
        """Ожидаемые данные из ответа order/simulate"""
        order_lines = self.api_order_simulate.get_order_lines()

        description_article_in_simulate = order_lines.description
        discount_distr = order_lines.distr_discount_percent
        sales_price_with_tax = order_lines.sales_price_with_tax
        expected_surcharges_percent = order_lines.surcharges_percent

        return ExpectedDataFromResponseSimulate(
            description_article_in_simulate,
            discount_distr,
            sales_price_with_tax,
            expected_surcharges_percent
        )

    def simulate(self, payload_simulate) -> list:
        """Отправляет запрос на simulate (добавление в корзину)"""
        # Отправляем запрос в order/simulate -> возвращаем объект objects

        self.api_order_simulate.post_order_simulate(payload_simulate)
        objects = self.api_order_simulate.get_objects_from_response(OrderSimulateModel)

        material_code_in_request_simulate = payload_simulate["materials"][0]["materialCode"]
        quantity_material_code_in_request_simulate = payload_simulate["materials"][0]["quantity"]
        print(f'\nДелаем POST запрос в корзину (добавление товара) на Order/Simulate. Код - '
              f'{material_code_in_request_simulate} Количество - {quantity_material_code_in_request_simulate}')

        return objects

    def order_create(self, payload_order_create) -> OrderCreateModel:
        """Отправляет запрос на order/create (создание заказа) и получает нужные поля"""
        #  Запрос на order/create
        print(f'Делаем запрос на order/create')

        self.api_order_create.post_order_create(payload_order_create)
        print()
        print(payload_order_create)
        print()
        objects_order_create = self.api_order_create.get_objects_from_response(OrderCreateModel)[0]
        orders = objects_order_create.orders[0]
        return orders

    def suit_of_check_field_api_full_commerce_new(self, payload_simulate, payload_order_create, offer_id, ):
        """Набор проверок полей api/CrmCommerce/fullCommerceNew"""
        expected_data_from_payload_order_create = self.expected_data_from_payload_order_create(payload_simulate,
                                                                                               payload_order_create)
        expected_data_from_response_order_simulate = self.expected_data_from_response_order_simulate()

        # Запрос на /api/CrmCommerce/FullCommerceNew и делаем проверки по полям
        api_full_commerce_new = FullCommerceNewApi()
        api_full_commerce_new.get_full_commerce_new_by_request_id(offer_id)
        api_full_commerce_new.check_code_material(expected_data_from_payload_order_create.expected_material_code)
        api_full_commerce_new.check_field_text_in_details(
            expected_data_from_response_order_simulate.description_article_in_simulate)
        api_full_commerce_new.check_discount_distr(expected_data_from_response_order_simulate.discount_distr)
        api_full_commerce_new.check_total_vat_in_data(expected_data_from_response_order_simulate.sales_price_with_tax)
        api_full_commerce_new.check_field_debtor_account_in_data(
            expected_data_from_payload_order_create.expected_debtor_account)
        api_full_commerce_new.check_field_currency_in_details(expected_data_from_payload_order_create.expected_currency)
        api_full_commerce_new.check_field_line_type_in_details(
            expected_data_from_payload_order_create.expected_line_type)
        api_full_commerce_new.check_field_code_in_payment_terms_in_object_orders(
            expected_data_from_payload_order_create.expected_payment_terms)
        api_full_commerce_new.check_field_condition_in_delivery_options_all_type_order(
            expected_data_from_payload_order_create.expected_delivery_condition,
            expected_data_from_payload_order_create.line_type_payload)
        api_full_commerce_new.check_field_delivery_cost_in_delivery_option_all_type_order(
            expected_data_from_payload_order_create.expected_delivery_cost,
            expected_data_from_payload_order_create.line_type_payload)
        api_full_commerce_new.check_field_total_delivery_weight_in_delivery_option_all_type_order(
            expected_data_from_payload_order_create.expected_total_delivery_weight,
            expected_data_from_payload_order_create.line_type_payload)
        api_full_commerce_new.check_field_delivery_comment_in_delivery_option_all_type_order(
            expected_data_from_payload_order_create.expected_delivery_comment,
            expected_data_from_payload_order_create.line_type_payload)
        api_full_commerce_new.check_field_delivery_end_point_in_delivery_option_all_type_order(
            expected_data_from_payload_order_create.expected_delivery_end_point,
            expected_data_from_payload_order_create.line_type_payload)
        api_full_commerce_new.check_field_desired_delivery_date_in_delivery_option_all_type_order(
            expected_data_from_payload_order_create.expected_desired_delivery_date,
            expected_data_from_payload_order_create.line_type_payload)
        api_full_commerce_new.check_field_delivery_full_set_only_in_delivery_option_all_type_order(
            expected_data_from_payload_order_create.expected_delivery_full_set_only,
            expected_data_from_payload_order_create.line_type_payload)
        api_full_commerce_new.check_field_cost_included_in_order_in_delivery_option_all_type_order(
            expected_data_from_payload_order_create.expected_cost_included_in_order,
            expected_data_from_payload_order_create.line_type_payload)
        api_full_commerce_new.check_field_consignee_id_in_delivery_option_all_type_order(
            expected_data_from_payload_order_create.expected_consignee_id,
            expected_data_from_payload_order_create.line_type_payload)
        api_full_commerce_new.check_field_surcharges_convertation_in_object_orders(
            expected_data_from_response_order_simulate.expected_surcharges_percent)

        # Проверка различных полей по типу заказа
        if expected_data_from_payload_order_create.order_type == 'Material':
            api_full_commerce_new.check_field_delivery_type_from_object_delivery_options(
                expected_data_from_payload_order_create.expected_delivery_type)
        elif expected_data_from_payload_order_create.order_type == 'HEX':
            api_full_commerce_new.check_field_delivery_type_from_object_delivery_options_dzr_prod(
                expected_data_from_payload_order_create.expected_delivery_type)
        elif expected_data_from_payload_order_create.order_type == 'AutoShield':
            api_full_commerce_new.check_field_delivery_type_from_object_delivery_options_prod(
                expected_data_from_payload_order_create.expected_delivery_type)
        elif expected_data_from_payload_order_create.order_type == 'HEXAdditions':
            api_full_commerce_new.check_field_delivery_type_from_object_delivery_options_hex(
                expected_data_from_payload_order_create.expected_delivery_type)

    @allure.title('Создание заказа из корзины с одним кодом, разные виды доставки, предоплата.')
    @pytest.mark.parametrize('payload_simulate, payload_order_create',
                             [
                                 pytest.param(tc['request_simulate'], tc['request_order_create'], id=tc['id'])
                                 for tc in TestCases.test_cases_prepayment
                             ]
                             )
    def test_create_order_with_one_code_different_types_of_delivery_from_cart_prepayment(
            self, payload_simulate: dict, payload_order_create: dict):
        """Создание заказа из корзины с одним кодом, разные виды доставки, предоплата.
        В данном тесте делаем запрос на order/simulate по коду материала -> получаем информацию о коде.
        Далее, отправляем запрос на order/create (создание заказа) с этим же кодом -> получаем необходимую
        информацию в ответе.
        После чего делаем запрос на /api/CrmCommerce/FullCommerceNew -> получение информации в деталях заказа.
        Сравниваем полученную информацию в симуляции с ответом от /api/CrmCommerce/FullCommerceNew.
        Сравниваем полученную информацию в /api/CrmCommerce/FullCommerceNew с информацией, которую отправляли
        в запросе на создание заказа order/create
        """
        # Запрос на order/simulate и получение объекта orderLine
        self.simulate(payload_simulate)

        #  Запрос на order/create
        orders = self.order_create(payload_order_create)

        offer_id = orders.offer_id
        print()
        print(offer_id, 'offer_id')

        self.suit_of_check_field_api_full_commerce_new(payload_simulate, payload_order_create, offer_id)

    @allure.title('Создание заказа из корзины на один код, разные условия доставки, кредит')
    def test_create_order_from_cart_with_one_code_different_types_of_delivery_credit(self):
        """Создание заказа из корзины на один код, разные условия доставки, кредит
        В данном тесте делаем запрос на order/simulate по коду материала -> получаем информацию о коде.
        Далее, отправляем запрос на order/create (создание заказа) с этим же кодом -> получаем необходимую
        информацию в ответе.
        После чего делаем запрос на /api/CrmCommerce/FullCommerceNew -> получение информации в деталях заказа.
        Сравниваем полученную информацию в симуляции с ответом от /api/CrmCommerce/FullCommerceNew.
        Сравниваем полученную информацию в /api/CrmCommerce/FullCommerceNew с информацией, которую отправляли
        в запросе на создание заказа order/create
        """
