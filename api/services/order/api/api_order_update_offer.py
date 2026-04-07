import json

from api_testing_project.services.base_api import BaseApi
from api_testing_project.services.endpoints import Endpoints


class ApiOrderUpdateOffer(BaseApi):
    """/api/Order/UpdateOfferCreateOffer"""

    def post_update_offer(self, data: json, headers=None):
        """Запрос Post на  /api/Order/UpdateOffer"""
        post_url = Endpoints.post_order_update_offer
        self.response_data = self.http_methods.post(url=post_url, body=data, headers=headers).json()

        return self.response_data
