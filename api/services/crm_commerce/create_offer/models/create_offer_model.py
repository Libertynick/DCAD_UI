from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from enum import Enum

from datetime import datetime

from pydantic.alias_generators import to_camel


# Перечисления для статуса ответа и подтипа
class StatusEnum(str, Enum):
    OK = "Ok"
    WARNING = "Warning"
    ERROR = "Error"


class SubTypeEnum(str, Enum):
    IMPORT = "Import"
    VEDA = "Veda"
    RIDAN = "Ridan"


class Schedule(BaseModel):
    isStandardHex: int = Field(..., description="Стандартный HEX.")
    onStockQty: float = Field(..., description="Количество на складе.")
    onTransitQty: float = Field(..., description="Количество в пути.")
    notAvaliableQty: float = Field(..., description="Недоступное количество.")
    transitDate: Optional[datetime] = Field(default=None, description="Дата транзита.")
    deliveryInfo: Optional[str] = Field(default=None, description="Информация о доставке.")


class Availability(BaseModel):
    schedule: Schedule = Field(..., description="ГрафикAvailability.")


class Item(BaseModel):
    # Указать необходимые поля для элемента
    pass


class BOMSet(BaseModel):
    item: Optional[List] = Field(default=None, description="Элемент БОМ.")


class Line(BaseModel):
    remark: Optional[str] = Field(default=None, description="Примечание.")
    availability: List[Availability] = Field(default=[], description="Список доступностей.")
    bomSet: Optional[BOMSet] = Field(default=None, description="Набор БОМ.")
    salesPrice: Optional[float] = Field(default=None, description="Цена продаж.")
    cost: Optional[float] = Field(default=None, description="Стоимость.")
    costCurrency: Optional[str] = Field(default=None, description="Валюта стоимости.")
    quantity: Optional[float] = Field(default=None, description="Количество.")
    description: Optional[str] = Field(default=None, description="Описание.")
    code: Optional[str] = Field(default=None, description="Код.")
    altMaterialCode: Optional[str] = Field(default=None, description="Альтернативный код материала.")
    totalWithDiscountSurchargesAndVAT: Optional[float] = Field(default=None,
                                                               description="Общая сумма с учетом скидок и НДС.")
    totalWithDiscountAndSurcharges: Optional[float] = Field(default=None, description="Общая сумма с учетом скидок.")
    totalWithDiscount: Optional[float] = Field(default=None, description="Общая сумма с учетом скидки.")
    surchargesDelayPercent: Optional[float] = Field(default=None, description="Процент задержки надбавок.")
    surchargesCurrencyConversionPercent: Optional[float] = Field(default=None,
                                                                 description="Процент конверсии надбавок.")
    discountAmount: Optional[float] = Field(default=None, description="Сумма скидки.")
    discountPercent: Optional[float] = Field(default=None, description="Процент скидки.")
    weight: Optional[float] = Field(default=None, description="Вес.")
    deliveryWeeks: int = Field(..., description="Недели доставки.")
    calcNumber: Optional[str] = Field(default=None, description="Номер расчета ТО.")
    calculationComment: Optional[str] = Field(default=None, description="Комментарий к расчету.")
    comment: Optional[str] = Field(default=None, description="Комментарий.")
    isSpecial: int = Field(..., description="Специальный статус.")
    isProtected: bool = Field(..., description="Защищённый статус.")
    calcId: Optional[str] = Field(default=None, description="ID расчета.")
    hexIsReady: bool = Field(..., description="Готовность HEX.")
    clientDiscountPercent: Optional[float] = Field(default=None, description="Процент скидки клиента.")
    clientBroughtAmountResult: Optional[float] = Field(default=None, description="Результат принесённой суммы клиента.")
    itpDiscountPercent: Optional[float] = Field(default=None, description="Процент скидки ИТП.")
    contractDiscountPercent: Optional[float] = Field(default=None, description="Процент скидки по контракту.")
    sourceNOrder: Optional[int] = Field(default=None, description="Исходный номер заказа.")
    positionOrder: int = Field(..., description="Номер позиции в заказе.")
    warrantyTotal: Optional[float] = Field(default=None, description="Общее количество гарантии.")
    salesPriceWithoutDiscount: float = Field(..., description="Цена за единицу без скидки.")
    totalWithoutDiscount: Optional[float] = Field(default=None, description="Общая сумма без скидки.")
    subType: SubTypeEnum = Field(..., description="Подтип позиции.")
    mpg: Optional[str] = Field(default=None, description="MPG.")
    prodHierarchy: Optional[str] = Field(default=None, description="Иерархия продукта.")
    category: Optional[str] = Field(default=None, description="Категория.")
    taxes: float = Field(..., description="Налоги.")
    abcCategory: Optional[str] = Field(default=None, description="ABC Категория.")
    equipmentCategoryId: Optional[str] = Field(default=None, description="ID категории оборудования.")
    equipmentCategory: Optional[str] = Field(default=None, description="Категория оборудования.")
    surchargePercent: Optional[float] = Field(default=None, description="Процент надбавки.")


class Offer(BaseModel):
    sapReferenceNumber: Optional[str] = Field(default=None, description="Ссылка на номер SAP.")
    paymentTerms: Optional[str] = Field(default=None, description="Условия оплаты.")
    exchangeRate: float = Field(..., description="Курс обмена.")
    deliveryPlant: Optional[str] = Field(default=None, description="Завод доставки.")
    deliveryMode: Optional[str] = Field(default=None, description="Способ доставки.")
    deliveryAddress: Optional[str] = Field(default=None, description="Адрес доставки.")
    debtorAccount: Optional[str] = Field(default=None, description="Счет дебитора.")
    currency: Optional[str] = Field(default=None, description="Валюта.")
    broughtAmountResult: float = Field(..., description="Результат принесённой суммы.")
    number: Optional[str] = Field(default=None, description="Номер предложения.")
    id: str = Field(..., description="ID предложения.")
    isITPsuccess: Optional[bool] = Field(default=None, description="Успех ИТП.")
    crmUrl: Optional[str] = Field(default=None, description="URL CRM.")
    clientBroughtAmountResult: Optional[float] = Field(default=None, description="Результат принесённой суммы клиента.")
    pObjectName: Optional[str] = Field(default=None, description="Имя объекта.")
    pObjectNumber: Optional[str] = Field(default=None, description="Номер объекта.")
    specificationNumber: Optional[str] = Field(default=None, description="Номер спецификации.")
    opportunityName: Optional[str] = Field(default=None, description="Имя возможности.")


class Invoice(BaseModel):
    id: str = Field(..., description="ID счета.")
    parentId: str = Field(..., description="ID родителя.")
    sapReferenceNumber: Optional[str] = Field(default=None, description="Номер SAP.")
    number: Optional[str] = Field(default=None, description="Номер сбытового документа.")


class Error(BaseModel):
    root: dict[str, str]  # Объект, содержащий ошибки


class ITPTip(BaseModel):
    name: Optional[str] = Field(default=None, description="Имя категории оборудования.")
    msg: int = Field(..., description="Сообщение: 0 - красное, 1 - желтое, 2 - зеленое.")
    warn: Optional[str] = Field(default=None, description="Подсказка.")


class CreatedOffer(BaseModel):
    id: Optional[str] = Field(default=None, description="ID созданного предложения.")
    number: Optional[str] = Field(default=None, description="Номер предложения.")


class Objects(BaseModel):
    lines: List[Line] = Field(default=[], description="Список позиций.")
    offers: List[Offer] = Field(default=[], description="Список предложений.")
    invoices: Optional[Invoice] = Field(default=None, description="Список счетов.")
    errors: Optional[Error] = Field(default=[], description="Список ошибок.")
    itPtips: Optional[ITPTip] = Field(default=[], description="Список подсказок ИТП.")
    createdOffers: Optional[CreatedOffer] = Field(default=[], description="Список созданных предложений.")


class ResponseModel(BaseModel):
    status: StatusEnum = Field(..., description="Статус ответа.")
    messages: List[str] = Field(default=[], description="Список сообщений или ошибок.")
    objects: List[Objects] = Field(..., description="Список объектов ответа.")

    model_config = ConfigDict(
        alias_generator=to_camel,
        use_enum_values=True
    )
