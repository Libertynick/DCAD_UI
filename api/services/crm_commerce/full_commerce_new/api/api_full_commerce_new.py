import uuid
from datetime import datetime
from uuid import UUID
from requests import Response

from api_testing_project.services.base_api import BaseApi
from api_testing_project.services.crm_commerce.full_commerce_new.models.full_commerce_new_model import \
    ModelFullCommerceNew, Data, Details, Order, DeliveryOptions, DeliveryOptionsDzrProd, \
    DeliveryOptionsProd, DeliveryOptionsHex, PaymentTerm


class FullCommerceNewApi(BaseApi):
    """API FullCommerceNew"""

    def get_full_commerce_new_by_request_id(self, order_id: UUID) -> Response:
        """Запрос GET к FullCommerceNew по id заказа"""
        get_url = self.endpoints.get_full_commerce_new(order_id)
        print(f'URL FullCommerceNew - {get_url}')
        self.response_data = self.http_methods.get(url=get_url).json()
        return self.response_data

    def get_details_object_from_response(self) -> Details:
        """Получение объекта details из ответа"""
        self.check_for_empty_data_from_response()

        details_full_commerce_new = self.get_objects_from_response(ModelFullCommerceNew)[0].details[0]
        return details_full_commerce_new

    def get_data_object_from_response(self) -> Data:
        """Получение объекта data из ответа"""
        self.check_for_empty_data_from_response()

        data_full_commerce_new = self.get_objects_from_response(ModelFullCommerceNew)[0].data[0]
        return data_full_commerce_new

    def get_orders_object_from_response(self) -> Order:
        """Получение объекта orders из ответа"""
        orders_full_commerce_new = self.get_data_object_from_response().orders[0]
        return orders_full_commerce_new

    def get_delivery_options_from_response(self) -> DeliveryOptions:
        """Получение объекта DeliveryOptions из ответа"""
        delivery_options_full_commerce_new = self.get_data_object_from_response().delivery_options
        return delivery_options_full_commerce_new

    def get_delivery_options_dzr_prod_from_response(self) -> DeliveryOptionsDzrProd:
        """Получение объекта deliveryOptionsDZRProd"""
        delivery_options_dzr_prod = self.get_data_object_from_response().delivery_options_d_z_r_prod
        assert delivery_options_dzr_prod is not None, "Не удалось получить объект DeliveryOptionsDZRProd"
        return delivery_options_dzr_prod

    def get_delivery_options_prod_from_response(self) -> DeliveryOptionsProd:
        """Получение объекта deliveryOptionsProd"""
        delivery_options_dzr_prod = self.get_data_object_from_response().delivery_options_prod
        assert delivery_options_dzr_prod is not None, "Не удалось получить объект DeliveryOptionsDZRProd"
        return delivery_options_dzr_prod

    def get_delivery_options_hex_from_response(self) -> DeliveryOptionsHex:
        """Получение объекта deliveryOptionsHex"""
        delivery_options_hex = self.get_data_object_from_response().delivery_options_hex
        assert delivery_options_hex is not None, "Не удалось получить объект DeliveryOptionsHex"
        return delivery_options_hex

    def get_payment_terms_from_response(self) -> PaymentTerm:
        """Получение объекта PaymentTerm"""
        payment_term = self.get_data_object_from_response().payment_term
        return payment_term

    def check_code_material(self, expected_code_material: str):
        """Проверка поля material_code"""
        details_full_commerce_new = self.get_details_object_from_response()
        material_code_in_full_commerce_new = details_full_commerce_new.code \
            if details_full_commerce_new.material_code is None else details_full_commerce_new.material_code

        assert material_code_in_full_commerce_new == expected_code_material, \
            f'Ожидаемый код материала из запроса - ({expected_code_material}) не соответствует коду материала ' \
            f'в деталях заказа (fullCommerceNew) - ({material_code_in_full_commerce_new})'

    def check_field_text_in_details(self, expected_description_article: str):
        """Проверка поля Описание (text) в объекте details"""
        expected_description_article = expected_description_article.replace(' ', '')

        details_full_commerce_new = self.get_details_object_from_response()
        material_code_in_full_commerce_new = details_full_commerce_new.material_code
        text_full_commerce_new = details_full_commerce_new.text.replace(' ', '')

        assert text_full_commerce_new == expected_description_article, \
            f'Описание кода {material_code_in_full_commerce_new} - ({text_full_commerce_new}) ' \
            f'в деталях заказа (fullCommerceNew) не соответствует описанию в симуляции - ' \
            f'({expected_description_article})'

    def check_discount_distr(self, expected_discount: float):
        """Проверка скидки дистра"""
        details_full_commerce_new = self.get_details_object_from_response()
        discount_distr = details_full_commerce_new.discount

        assert expected_discount == discount_distr, \
            f'Скидки в деталях заказа (fullCommerceNew) - {discount_distr} не соответствуют скидкам ' \
            f'в корзине (order/simulate) - {expected_discount}'

    def check_total_vat_in_data(self, expected_total_vat: float, id_order: str = None):
        """Проверка значения поля Итого с НДС total_vat"""
        total_vat_in_details_order = self.get_data_object_from_response().total_vat

        assert abs(total_vat_in_details_order - expected_total_vat) < 0.5, \
            f'Итоговая сумма в деталях заказа {id_order} (fullCommerceNew) - ({total_vat_in_details_order}) не соответствует ' \
            f'итоговой сумме в корзине (order/simulate) - ({expected_total_vat})'

    def check_field_debtor_account_in_data(self, expected_debtor_account: str):
        """Проверка поля Номер договора (debtor_account) в объекте data"""
        debtor_account = self.get_data_object_from_response().debtor_account

        assert expected_debtor_account == debtor_account, \
            f'Номер договора клиента в деталях заказа (fullCommerceNew) - ({debtor_account}) ' \
            f'не соответствует ожидаемому из запроса в create/order - ({expected_debtor_account})'

    def check_field_currency_in_details(self, expected_currency: str):
        """Проверка поля Валюта (currency) в объекте details"""
        currency = self.get_details_object_from_response().currency

        assert expected_currency == currency, \
            f'Валюта в деталях заказа (fullCommerceNew) - ({currency}) не соответствует ' \
            f'ожидаемой в запросе create/order - ({expected_currency})'

    def check_field_delivery_type_from_object_delivery_options(self, expected_delivery_type: str):
        """Проверка поля Способ доставки в объекте DeliveryOptions"""
        delivery_type = self.get_delivery_options_from_response().delivery_type

        assert expected_delivery_type == delivery_type, \
            f'Условия доставки в запросе create/order - ({expected_delivery_type}) не соответствуют условиям ' \
            f'на странице детали заказа (fullCommerceNew) - ({delivery_type})'

    def check_field_delivery_type_from_object_delivery_options_dzr_prod(self, expected_delivery_options_dzr_prod: str):
        """Проверка поля Способ доставки ПТО в объекте DeliveryOptionsDZRProd"""
        delivery_type = self.get_delivery_options_dzr_prod_from_response().delivery_type

        assert expected_delivery_options_dzr_prod == delivery_type, \
            f'Условия доставки в запросе create/order - ({expected_delivery_options_dzr_prod}) не соответствуют условиям ' \
            f'на странице детали заказа (fullCommerceNew) - ({delivery_type})'

    def check_field_delivery_type_from_object_delivery_options_prod(self, expected_delivery_options_prod):
        """Проверка поля Способ доставки ПТО в объекте DeliveryOptionsProd"""
        delivery_type = self.get_delivery_options_prod_from_response().delivery_type

        assert expected_delivery_options_prod == delivery_type, \
            f'Условия доставки в запросе create/order - ({expected_delivery_options_prod}) не соответствуют условиям ' \
            f'на странице детали заказа (fullCommerceNew) - ({delivery_type})'

    def check_field_delivery_type_from_object_delivery_options_hex(self, expected_delivery_options_hex):
        """Проверка поля deliveryType Способ доставки ПТО в объекте DeliveryOptionsProd"""
        delivery_type = self.get_delivery_options_hex_from_response().delivery_type

        assert expected_delivery_options_hex == delivery_type, \
            f'Условия доставки в запросе create/order - ({expected_delivery_options_hex}) не соответствуют условиям ' \
            f'на странице детали заказа (fullCommerceNew) - ({delivery_type})'

    def check_field_line_type_in_details(self, expected_line_type: str):
        """Проверка поля lineType в объекте details"""
        line_type = self.get_details_object_from_response().line_type

        assert expected_line_type == line_type, \
            f'Поле lineType на странице Детали заказа (fullCommerceNew) - ({line_type}) не соответствует lineType ' \
            f'из запроса на создание заказа create/order - ({expected_line_type})'

    def check_field_code_in_payment_terms_in_object_orders(self, expected_code_payment_terms: str):
        """Проверка поля code в payment_terms (код условий оплаты) в объекте orders"""
        code_payment_term = self.get_payment_terms_from_response().code

        assert expected_code_payment_terms == code_payment_term, \
            f'Поле code в PaymentTerm на странице Детали заказа (fullCommerceNew) - ({code_payment_term}) ' \
            f'не соответствует ожидаемому - ({expected_code_payment_terms})'

    def check_field_condition_in_delivery_options_all_type_order(self, expected_condition: str,
                                                                 line_type_in_payload: str):
        """Проверка поля condition в объекте deliveryOption по всем типам заказа
        line_type_in_payload - поле в запросе в объекте order_lines
        """
        condition = None
        if line_type_in_payload == 'Material':
            condition = self.get_delivery_options_from_response().condition
        elif line_type_in_payload == 'HEXAdditions':
            condition = self.get_delivery_options_hex_from_response().condition
        elif line_type_in_payload in ['HEX', 'Pump']:
            condition = self.get_delivery_options_dzr_prod_from_response().condition
        elif line_type_in_payload in ['AutoShield', 'TDU', 'BTP']:
            condition = self.get_delivery_options_prod_from_response().condition

        assert condition == expected_condition, \
            f'Поле condition в объекте deliveryOption на странице Детали заказа (fullCommerceNew) - ({condition}) ' \
            f'не соответствует ожидаемому - ({expected_condition})'

    def check_field_delivery_cost_in_delivery_option_all_type_order(self, expected_delivery_cost: float,
                                                                    line_type_in_payload: str):
        """Проверка поля delivery_cost в объекте deliveryOption по всем типам заказа
        line_type_in_payload - поле в запросе в объекте order_lines
        """
        delivery_cost = 0.0

        if line_type_in_payload == 'Material':
            delivery_cost = self.get_delivery_options_from_response().delivery_cost
        elif line_type_in_payload == 'HEXAdditions':
            delivery_cost = self.get_delivery_options_hex_from_response().delivery_cost
        elif line_type_in_payload in ['HEX', 'Pump']:
            delivery_cost = self.get_delivery_options_dzr_prod_from_response().delivery_cost
        elif line_type_in_payload in ['AutoShield', 'TDU', 'BTP']:
            delivery_cost = self.get_delivery_options_prod_from_response().delivery_cost

        assert expected_delivery_cost == delivery_cost, \
            f'Поле delivery_cost в объекте deliveryOption на странице Детали заказа (fullCommerceNew) - ({delivery_cost})' \
            f' не соответствует ожидаемому - ({expected_delivery_cost})'

    def check_field_total_delivery_weight_in_delivery_option_all_type_order(self, expected_total_delivery_weight: None,
                                                                            line_type_in_payload: str):
        """Проверка поля total_delivery_weight в объекте deliveryOption по всем типам заказа
        line_type_in_payload - поле в запросе в объекте order_lines
        """
        total_delivery_weight = None

        if line_type_in_payload == 'Material':
            total_delivery_weight = self.get_delivery_options_from_response().total_delivery_weight
        elif line_type_in_payload == 'HEXAdditions':
            total_delivery_weight = self.get_delivery_options_hex_from_response().total_delivery_weight
        elif line_type_in_payload in ['HEX', 'Pump']:
            total_delivery_weight = self.get_delivery_options_dzr_prod_from_response().total_delivery_weight
        elif line_type_in_payload in ['AutoShield', 'TDU', 'BTP']:
            total_delivery_weight = self.get_delivery_options_prod_from_response().total_delivery_weight

        assert expected_total_delivery_weight == total_delivery_weight, \
            f'Поле total_delivery_weight в объекте deliveryOption на странице Детали заказа (fullCommerceNew) - ' \
            f'({total_delivery_weight}) не соответствует ожидаемому - ({expected_total_delivery_weight})'

    def check_field_delivery_comment_in_delivery_option_all_type_order(self, expected_delivery_comment: str,
                                                                       line_type_in_payload: str):
        """Проверка поля delivery_comment в объекте deliveryOption по всем типам заказа
        line_type_in_payload - поле в запросе в объекте order_lines
        """
        delivery_comment = ''

        if line_type_in_payload == 'Material':
            delivery_comment = self.get_delivery_options_from_response().comment
        elif line_type_in_payload == 'HEXAdditions':
            delivery_comment = self.get_delivery_options_hex_from_response().comment
        elif line_type_in_payload in ['HEX', 'Pump']:
            delivery_comment = self.get_delivery_options_dzr_prod_from_response().comment
        elif line_type_in_payload in ['AutoShield', 'TDU', 'BTP']:
            delivery_comment = self.get_delivery_options_prod_from_response().comment

        assert expected_delivery_comment == delivery_comment, \
            f'Поле delivery_comment в объекте deliveryOption на странице Детали заказа (fullCommerceNew) - ' \
            f'({delivery_comment}) не соответствует ожидаемому - ({expected_delivery_comment})'

    def check_field_delivery_end_point_in_delivery_option_all_type_order(self, expected_delivery_end_point: str,
                                                                         line_type_in_payload: str):
        """Проверка поля delivery_end_point в объекте deliveryOption по всем типам заказа
        line_type_in_payload - поле в запросе в объекте order_lines
        """
        delivery_end_point = ''

        if line_type_in_payload == 'Material':
            delivery_end_point = self.get_delivery_options_from_response().end_point
        elif line_type_in_payload == 'HEXAdditions':
            delivery_end_point = self.get_delivery_options_hex_from_response().end_point
        elif line_type_in_payload in ['HEX', 'Pump']:
            delivery_end_point = self.get_delivery_options_dzr_prod_from_response().end_point
        elif line_type_in_payload in ['AutoShield', 'TDU', 'BTP']:
            delivery_end_point = self.get_delivery_options_prod_from_response().end_point

        assert expected_delivery_end_point == delivery_end_point, \
            f'Поле delivery_end_point в объекте deliveryOption на странице Детали заказа (fullCommerceNew) - ' \
            f'({delivery_end_point}) не соответствует ожидаемому - ({expected_delivery_end_point})'

    def check_field_desired_delivery_date_in_delivery_option_all_type_order(self, expected_desired_delivery_date: None,
                                                                            line_type_in_payload: str):
        """Проверка поля desired_delivery_date в объекте deliveryOption по всем типам заказа
        line_type_in_payload - поле в запросе в объекте order_lines
        """
        desired_delivery_date = None

        if line_type_in_payload == 'Material':
            desired_delivery_date = self.get_delivery_options_from_response().desired_delivery_date
        elif line_type_in_payload == 'HEXAdditions':
            desired_delivery_date = self.get_delivery_options_hex_from_response().desired_delivery_date
        elif line_type_in_payload in ['HEX', 'Pump']:
            desired_delivery_date = self.get_delivery_options_dzr_prod_from_response().desired_delivery_date
        elif line_type_in_payload in ['AutoShield', 'TDU', 'BTP']:
            desired_delivery_date = self.get_delivery_options_prod_from_response().desired_delivery_date

        expected_desired_delivery_date = datetime.fromisoformat(str(expected_desired_delivery_date))
        assert expected_desired_delivery_date == desired_delivery_date, \
            f'Поле desired_delivery_date в объекте deliveryOption на странице Детали заказа (fullCommerceNew) - ' \
            f'({desired_delivery_date}) не соответствует ожидаемому - ({expected_desired_delivery_date})'

    def check_field_delivery_full_set_only_in_delivery_option_all_type_order(self,
                                                                             expected_delivery_full_set_only: None,
                                                                             line_type_in_payload: str):
        """Проверка поля delivery_full_set_only в объекте deliveryOption по всем типам заказа
        line_type_in_payload - поле в запросе в объекте order_lines
        """
        delivery_full_set_only = None

        if line_type_in_payload == 'Material':
            delivery_full_set_only = self.get_delivery_options_from_response().deliver_full_set_only
        elif line_type_in_payload == 'HEXAdditions':
            delivery_full_set_only = self.get_delivery_options_hex_from_response().deliver_full_set_only
        elif line_type_in_payload in ['HEX', 'Pump']:
            delivery_full_set_only = self.get_delivery_options_dzr_prod_from_response().deliver_full_set_only
        elif line_type_in_payload in ['AutoShield', 'TDU', 'BTP']:
            delivery_full_set_only = self.get_delivery_options_prod_from_response().deliver_full_set_only

        assert expected_delivery_full_set_only == delivery_full_set_only, \
            f'Поле delivery_full_set_only в объекте deliveryOption на странице Детали заказа (fullCommerceNew) - ' \
            f'({delivery_full_set_only}) не соответствует ожидаемому - ({expected_delivery_full_set_only})'

    def check_field_cost_included_in_order_in_delivery_option_all_type_order(self,
                                                                             expected_cost_included_in_order: None,
                                                                             line_type_in_payload: str):
        """Проверка поля cost_included_in_order в объекте deliveryOption по всем типам заказа
        line_type_in_payload - поле в запросе в объекте order_lines
        """
        cost_included_in_order = None

        if line_type_in_payload == 'Material':
            cost_included_in_order = self.get_delivery_options_from_response().cost_included_in_order
        elif line_type_in_payload == 'HEXAdditions':
            cost_included_in_order = self.get_delivery_options_hex_from_response().cost_included_in_order
        elif line_type_in_payload in ['HEX', 'Pump']:
            cost_included_in_order = self.get_delivery_options_dzr_prod_from_response().cost_included_in_order
        elif line_type_in_payload in ['AutoShield', 'TDU', 'BTP']:
            cost_included_in_order = self.get_delivery_options_prod_from_response().cost_included_in_order

        assert expected_cost_included_in_order == cost_included_in_order, \
            f'Поле cost_included_in_order в объекте deliveryOption на странице Детали заказа (fullCommerceNew) - ' \
            f'({cost_included_in_order}) не соответствует ожидаемому - ({expected_cost_included_in_order})'

    def check_field_consignee_id_in_delivery_option_all_type_order(self,
                                                                   expected_consignee_id: None,
                                                                   line_type_in_payload: str):
        """Проверка поля consignee_id в объекте deliveryOption по всем типам заказа
        line_type_in_payload - поле в запросе в объекте order_lines
        """
        consignee_id = None

        if line_type_in_payload == 'Material':
            consignee_id = self.get_delivery_options_from_response().consignee_id
        elif line_type_in_payload == 'HEXAdditions':
            consignee_id = self.get_delivery_options_hex_from_response().consignee_id
        elif line_type_in_payload in ['HEX', 'Pump']:
            consignee_id = self.get_delivery_options_dzr_prod_from_response().consignee_id
        elif line_type_in_payload in ['AutoShield', 'TDU', 'BTP']:
            consignee_id = self.get_delivery_options_prod_from_response().consignee_id

        if expected_consignee_id is None:
            assert consignee_id is not None, f'Поле consignee_id в объекте DeliveryOption - null'

        else:
            expected_consignee_id = uuid.UUID(expected_consignee_id)
            assert expected_consignee_id == consignee_id, \
                f'Поле consignee_id в объекте deliveryOption на странице Детали заказа (fullCommerceNew) - ' \
                f'({consignee_id}) не соответствует ожидаемому - ({expected_consignee_id})'

    def check_field_surcharges_convertation_in_object_orders(self, expected_surcharges_convertation):
        """Проверка поля surchargesConvertation в объекте orders"""
        data = self.get_data_object_from_response()
        surcharges_convertation = data.surcharges_convertation

        assert surcharges_convertation == expected_surcharges_convertation, \
            f'Поле surchargesConvertation в fullCommerceNew (Детали заказа) - ({surcharges_convertation}) не ' \
            f'соответствует ожидаемому - ({expected_surcharges_convertation})'
