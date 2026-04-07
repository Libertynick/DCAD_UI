import json

from api_testing_project.services.base_api import BaseApi


class ApiCommerceList(BaseApi):
    """/api/CrmCommerce/CommerceList"""

    def post_commerce_list(self, data: json, headers=None):
        """Запрос POST на /api/CrmCommerce/CommerceList"""
        post_url = self.endpoints.post_commerce_list
        self.response_data = self.http_methods.post(url=post_url, body=data, headers=headers).json()
        return self.response_data