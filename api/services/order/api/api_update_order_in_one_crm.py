from api_testing_project.services.base_api import BaseApi
from api_testing_project.services.endpoints import Endpoints


class ApiUpdateOrderInOneCrm(BaseApi):
    """/api/Offer/UpdateOrderInOneCrm"""

    def post_update_order_in_one_crm(self, data, headers=None):
        """Запрос POST на /api/Offer/UpdateOrderInOneCrm"""
        post_url = Endpoints.post_update_order_in_one_crm
        self.response_data = self.http_methods.post(url=post_url, body=data, headers=headers).json()

        return self.response_data