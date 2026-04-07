from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from enum import Enum


class Status(str, Enum):
    OK = "Ok"
    WARNING = "Warning"
    ERROR = "Error"


class Offer(BaseModel):
    offer_id: UUID = Field(..., alias='offerId', description="ID из OneCRM")
    offer_number: Optional[str] = Field(None, alias='offerNumber', description="Номер документа в OneCRM")


class Order(BaseModel):
    offer_id: UUID = Field(..., alias='offerId', description="ID из OneCRM")
    offer_number: Optional[str] = Field(None, alias='offerNumber', description="Номер документа в OneCRM")
    order_number: Optional[str] = Field(None, alias='orderNumber', description="Номер заказа в 1С")
    order_type: str = Field(..., alias='orderType', description="Тип заказа", enum={"Common", "HEX", "BTP"})


class ResponseObject(BaseModel):
    id: Optional[UUID] = Field(None, description="DEPRECATED. Id из OneCRM")
    doc_number: Optional[str] = Field(None, alias='docNumber',
                                      description="DEPRECATED. Номер документа, созданного в SAP")
    reference_number: Optional[str] = Field(None, alias='referenceNumber',
                                            description="DEPRECATED. Ссылочный номер, использовавшийся для создания документа SAP")
    hex_reference_numbers: List[str] = Field(..., alias='hexReferenceNumbers',
                                             description="DEPRECATED. Ссылочные номера заказов теплообменников")
    offer: Offer = Field(..., description="Информация о предложении")
    orders: List[Order] = Field(..., description="Список заказов, созданных по этому базовому КП")


class OrderCreateModel(BaseModel):
    status: Status = Field(..., description="Статус ответа")
    messages: List[str] = Field(..., description="Список сообщений или ошибок, возникших в процессе обработки запроса")
    objects: List[ResponseObject] = Field(..., description="Ответ с результатом создания заказа")
