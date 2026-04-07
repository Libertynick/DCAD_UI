import json

from api_testing_project.services.base_api import BaseApi
from api_testing_project.services.endpoints import Endpoints


class ApiUpdateMaterials(BaseApi):
    """api/Material/UpdateMaterials"""

    def post_update_materials(self, data: json):
        """Запрос POST на api/Material/UpdateMaterials"""
        post_url = Endpoints.post_update_materials
        res_post = self.http_methods.post(post_url, data)
        self.response_data = res_post.json()
        return res_post
