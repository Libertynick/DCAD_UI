from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from enum import Enum


class Status(str, Enum):
    """Enum для статуса ответа"""
    OK = "Ok"
    WARNING = "Warning"
    ERROR = "Error"


class UpdateOrderObject(BaseModel):
    """Объект с данными обновленного заказа"""
    order_number: Optional[str] = Field(None, alias='orderNumber', description="Номер заказа")
    offer_id: UUID = Field(..., alias='offerId', description="ID оффера из OneCRM")
    offer_number: Optional[str] = Field(None, alias='offerNumber', description="Номер оффера в OneCRM")


class UpdateOrderInOneCrmModel(BaseModel):
    """Модель ответа для /api/Offer/UpdateOrderInOneCrm"""
    status: Status = Field(..., description="Статус ответа")
    messages: List[str] = Field(..., description="Список сообщений или ошибок, возникших в процессе обработки запроса")
    objects: List[UpdateOrderObject] = Field(..., description="Ответ с результатом обновления заказа")