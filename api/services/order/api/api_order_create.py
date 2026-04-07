import json

import allure

from api_testing_project.services.base_api import BaseApi
from api_testing_project.services.endpoints import Endpoints
from api_testing_project.services.order.models.order_create_model import OrderCreateModel


class ApiOrderCreate(BaseApi):
    """api/order/create"""

    def post_order_create(self, data: json):
        """Запрос POST на api/order/create"""
        post_url = Endpoints.post_order_create
        self.response_data = self.http_methods.post(post_url, body=data).json()

        return self.response_data

    def get_offer_number(self) -> str:
        """Получение значения поля offerNumber"""
        with allure.step('api/order/create. Получение значения поля offerNumber'):
            self.check_for_empty_data_from_response()

            orders = self.get_objects_from_response(OrderCreateModel)[0].orders
            offer_number = orders[0].offer_number

            return offer_number

    def get_offer_id(self) -> str:
        """Получение значения из поля offerId"""
        with allure.step('api/order/create. '):
            self.check_for_empty_data_from_response()

            orders = self.get_objects_from_response(OrderCreateModel)[0].orders
            offer_id = orders[0].offer_id

            return str(offer_id)
