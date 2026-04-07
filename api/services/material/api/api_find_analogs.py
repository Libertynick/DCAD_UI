import json

from api_testing_project.services.base_api import BaseApi
from api_testing_project.services.endpoints import Endpoints


class ApiFindAnalogs(BaseApi):
    """api/Material/FindAnalogs"""

    def post_find_analogs(self, data: json):
        """Запрос POST на api/Material/FindAnalogs"""
        post_url = Endpoints.post_find_analogs
        res_post = self.http_methods.post(post_url, data)
        self.response_data = res_post.json()
        return res_post