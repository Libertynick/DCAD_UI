from api_testing_project.services.base_api import BaseApi
from api_testing_project.services.endpoints import Endpoints


class ApiGetMaterialDocument(BaseApi):
    """api/Material/GetMaterialDocument"""

    def get_material_document(self, material_code: str, file_name: str):
        """Запрос GET на api/Material/GetMaterialDocument"""
        get_url = self.endpoints.get_material_document(material_code, file_name)
        print(f'URL GetMaterialDocument - {get_url}')
        res_get = self.http_methods.get(url=get_url)
        return res_get