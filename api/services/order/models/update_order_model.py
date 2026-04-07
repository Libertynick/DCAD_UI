from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class StatusEnum(str, Enum):
    """
    Enum для статуса ответа.

    Возможные значения:
    - Ok: Запрос успешно обработан.
    - Warning: Обработка запроса завершилась с предупреждением.
    - Error: Обработка запроса завершилась с ошибкой.
    """
    ok = "Ok"
    warning = "Warning"
    error = "Error"


class ObjectResponse(BaseModel):
    """
    Модель для стандартного ответа, содержащего статус.

    Attributes:
    - status (bool): Статус ответа для данного объекта (True или False).
    """
    status: bool = Field(..., description='Статус ответа.')


class ResponseModelUpdateOffer(BaseModel):
    """
    Основная модель для описания формата ответа API.

    Attributes:
    - status (StatusEnum): Статус ответа, указывающий на результат обработки запроса.
    - messages (List[str]): Список сообщений или ошибок, возникших в процессе обработки запроса.
    - objects (List[ObjectResponse]): Список объектов с ответом, где каждый объект имеет свой статус.
    """
    status: StatusEnum = Field(..., description='Статус ответа')
    messages: List[str] = Field(default=[], description='Список сообщений или ошибок')
    objects: List[ObjectResponse] = Field(..., description='Список объектов с ответом')
