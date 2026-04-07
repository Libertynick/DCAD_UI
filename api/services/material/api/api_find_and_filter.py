import json

from api_testing_project.services.base_api import BaseApi
from api_testing_project.services.endpoints import Endpoints


class ApiFindAndFilter(BaseApi):
    """api/Material/FindAndFilter"""

    def post_find_and_filter(self, data: json):
        """Запрос POST на api/Material/FindAndFilter"""
        post_url = Endpoints.post_find_and_filter
        res_post = self.http_methods.post(post_url, data)
        self.response_data = res_post.json()
        return res_post