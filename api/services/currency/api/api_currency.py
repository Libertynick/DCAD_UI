from api_testing_project.services.base_api import BaseApi
from api_testing_project.services.currency.models.get_conventional_units_models import GetConventionalUnitsModel
from api_testing_project.services.endpoints import Endpoints
from api_testing_project.utils.http_methods import HttpMethods


class CurrencyApi(BaseApi):
    """API Currency"""

    def get_conventional_units(self, exchange_rate_type: str):
        """API GetConventionalUnits"""
        get_url = self.endpoints.get_conventional_units(exchange_rate_type)
        print(f'URL GetConventionalUnits - {get_url}')
        self.response_data = self.http_methods.get(url=get_url).json()
        return self.response_data
