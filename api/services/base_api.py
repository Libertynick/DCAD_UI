from typing import List, Any

from pydantic_core import ValidationError

from api_testing_project.services.endpoints import Endpoints
from api_testing_project.utils.http_methods import HttpMethods


class BaseApi:
    """Базовые методы для api"""

    def __init__(self):
        self.response_data = None  # Атрибут для хранения данных ответа
        self.http_methods = HttpMethods()
        self.endpoints = Endpoints()

    def check_for_empty_data_from_response(self):
        """Проверка на пустоту данных из ответа"""
        if self.response_data is None:
            raise ValueError("Response data not available. Please call api first.")

    def get_objects_from_response(self, class_model: Any) -> List:
        """Получение Objects из сохраненного ответа"""
        self.check_for_empty_data_from_response()
        try:
            json_response = class_model(**self.response_data)
            objects = json_response.objects
            return objects
        except ValidationError as e:
            raise ValueError(f'{e}\n Ошибка валидации полей из ответа.')

    def get_field_status_from_response(self, class_model: Any) -> str:
        """Получение поля status из ответа"""
        self.check_for_empty_data_from_response()

        json_response = class_model(**self.response_data)
        status = json_response.status

        return status

    def get_messages_from_response(self, class_model: Any) -> list:
        """Получение поля messages из ответа"""
        self.check_for_empty_data_from_response()

        json_response = class_model(**self.response_data)
        messages = json_response.messages

        return messages
