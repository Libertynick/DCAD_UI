import json

from api_testing_project.services.base_api import BaseApi
from api_testing_project.services.endpoints import Endpoints


class ApiReservationThresholdUpdate(BaseApi):
    """/api/Customer/ReservationThresholdUpdate"""

    def update_reservation_threshold(self, request: json, headers: json = None):
        """Обновление данных о резервации"""
        post_rl = Endpoints.post_reservation_threshold_update
        self.response_data = self.http_methods.post(url=post_rl, body=request, headers=headers)

        return self.response_data
