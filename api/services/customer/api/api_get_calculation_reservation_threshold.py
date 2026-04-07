import json

from api_testing_project.services.base_api import BaseApi
from api_testing_project.services.endpoints import Endpoints


class ApiGetCalculationReservationThreshold(BaseApi):
    """/api/Customer/GetCalculationReservationThreshold"""

    def get_calculation_reservation_threshold(self, contract_number: str, headers: json = None) -> json:
        """
        Получить посчитанный остаток резерва
        :param contract_number: Номер договора
        :param headers: Заголовки
        """
        get_url = Endpoints.get_calculation_reservation_threshold(self, contract_number=contract_number)
        print(get_url)
        self.response_data = self.http_methods.get(url=get_url, headers=headers).json()

        return self.response_data
