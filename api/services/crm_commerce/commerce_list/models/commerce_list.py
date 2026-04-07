from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from enum import Enum


class Status(str, Enum):
    OK = "Ok"
    WARNING = "Warning"
    ERROR = "Error"


class Source(str, Enum):
    CRM = "CRM"
    CSD = "CSD"
    WebClient = "WebClient"


class OfferType(str, Enum):
    PQ = "PQ"
    BTP = "BTP"
    IND = "IND"
    HR = "HR"
    CLH = "CLH"


class Money(BaseModel):
    value: float = Field(..., description="Сумма")
    currency: str = Field(..., description="Валюта")

    model_config = ConfigDict(
        alias_generator=lambda x: x[0].lower() + x[1:] if x else x,
    )


class DeliveryStatus(BaseModel):
    id: UUID = Field(..., description="ID статуса доставки")
    value: str = Field(..., description="Название статуса доставки")

    model_config = ConfigDict(
        alias_generator=lambda x: x[0].lower() + x[1:] if x else x,
    )


class Person(BaseModel):
    person_id: UUID = Field(..., alias="personId", description="ID персоны")
    name: str = Field(..., description="Имя")
    sur_name: str = Field(..., alias="surName", description="Фамилия")
    phone_number: Optional[str] = Field(None, alias="phoneNumber", description="Телефон")
    email: Optional[str] = Field(None, description="Email")
    is_main_responsible_person: bool = Field(..., alias="isMainResponsiblePerson", description="Основной ответственный")

    model_config = ConfigDict(
        alias_generator=lambda x: x[0].lower() + x[1:] if x else x,
    )


class PassportObject(BaseModel):
    id: Optional[str] = Field(None, description="ID паспорта")
    number: Optional[str] = Field(None, description="Номер паспорта")
    name: Optional[str] = Field(None, description="Название паспорта")
    address: Optional[str] = Field(None, description="Адрес")
    responsible_person: Optional[Person] = Field(None, alias="responsiblePerson", description="Ответственное лицо")

    model_config = ConfigDict(
        alias_generator=lambda x: x[0].lower() + x[1:] if x else x,
    )


class OfferStatus(BaseModel):
    id: UUID = Field(..., description="ID статуса КП")
    value: str = Field(..., description="Название статуса")

    model_config = ConfigDict(
        alias_generator=lambda x: x[0].lower() + x[1:] if x else x,
    )


class EngSpecType(BaseModel):
    id: UUID = Field(..., description="ID типа инженерной спецификации")
    value: str = Field(..., description="Название типа")

    model_config = ConfigDict(
        alias_generator=lambda x: x[0].lower() + x[1:] if x else x,
    )


class PurchaseType(BaseModel):
    id: UUID = Field(..., description="ID типа покупки")
    value: str = Field(..., description="Название типа покупки")

    model_config = ConfigDict(
        alias_generator=lambda x: x[0].lower() + x[1:] if x else x,
    )


class DistrRequest(BaseModel):
    id: str = Field(..., description="ID запроса дистрибьютора")
    number: str = Field(..., description="Номер запроса")
    creator: Person = Field(..., description="Создатель запроса")
    responsible_person: Person = Field(..., alias="responsiblePerson", description="Ответственное лицо")

    model_config = ConfigDict(
        alias_generator=lambda x: x[0].lower() + x[1:] if x else x,
    )


class PaymentTerm(BaseModel):
    code: str = Field(..., description="Код условий оплаты")
    text: str = Field(..., description="Описание условий")
    credit_days: Optional[int] = Field(None, alias="creditDays", description="Дни кредита")
    prepay_percent: int = Field(..., alias="prepayPercent", description="Процент предоплаты")

    model_config = ConfigDict(
        alias_generator=lambda x: x[0].lower() + x[1:] if x else x,
    )


class Approver(BaseModel):
    person_id: UUID = Field(..., alias="personId", description="ID согласующего")
    email: str = Field(..., description="Email")
    phone: str = Field(..., description="Телефон")
    name: str = Field(..., description="Имя")

    model_config = ConfigDict(
        alias_generator=lambda x: x[0].lower() + x[1:] if x else x,
    )


class Organization(BaseModel):
    contractor_id: UUID = Field(..., alias="contractorId", description="ID контрагента")
    inn: str = Field(..., description="ИНН")
    contractor_name: str = Field(..., alias="contractorName", description="Название контрагента")
    approvers: Optional[List[Approver]] = Field(None, description="Согласующие")

    model_config = ConfigDict(
        alias_generator=lambda x: x[0].lower() + x[1:] if x else x,
    )


class Delivery(BaseModel):
    short_info: str = Field(..., alias="shortInfo", description="Краткая информация о доставке")
    address: Optional[str] = Field(None, description="Адрес доставки")
    cost: float = Field(..., description="Стоимость доставки")
    cost_currency: str = Field(..., alias="costCurrency", description="Валюта доставки")
    deliver_full_set_only: bool = Field(..., alias="deliverFullSetOnly", description="Доставка только полным комплектом")

    model_config = ConfigDict(
        alias_generator=lambda x: x[0].lower() + x[1:] if x else x,
    )


class PaidStorage(BaseModel):
    tariff: float = Field(..., description="Тариф")
    sum: float = Field(..., description="Сумма")
    date_begin: str = Field(..., alias="dateBegin", description="Дата начала")
    date_end: str = Field(..., alias="dateEnd", description="Дата окончания")
    storage_invoice_number: str = Field(..., alias="storageInvoiceNumber", description="Номер счета")
    storage_invoice_date: datetime = Field(..., alias="storageInvoiceDate", description="Дата счета")

    model_config = ConfigDict(
        alias_generator=lambda x: x[0].lower() + x[1:] if x else x,
    )


class Offer(BaseModel):
    id: UUID = Field(..., description="ID КП")
    number: str = Field(..., description="Номер КП")
    c_date: datetime = Field(..., alias="cDate", description="Дата создания")
    u_date: datetime = Field(..., alias="uDate", description="Дата обновления")
    source: Optional[Source] = Field(None, description="Источник")
    validity_display: datetime = Field(..., alias="validityDisplay", description="Срок действия")
    is_valid: bool = Field(..., alias="isValid", description="Действителен")
    total_delivered_amount: Money = Field(..., alias="totalDeliveredAmount", description="Сумма отгруженного")
    delivery_status: DeliveryStatus = Field(..., alias="deliveryStatus", description="Статус доставки")
    offer_flags: List[str] = Field(..., alias="offerFlags", description="Флаги КП")
    debtor_account: Optional[str] = Field(None, alias="debtorAccount", description="Дебиторский счет")
    reference_number: str = Field(..., alias="referenceNumber", description="Референсный номер")
    total_offer_amount: Money = Field(..., alias="totalOfferAmount", description="Общая сумма КП")
    distributor_name: str = Field(..., alias="distributorName", description="Название дистрибьютора")
    distributor_inn: str = Field(..., alias="distributorINN", description="ИНН дистрибьютора")
    end_client_name: Optional[str] = Field(None, alias="endClientName", description="Название конечного клиента")
    end_client_inn: Optional[str] = Field(None, alias="endClientINN", description="ИНН конечного клиента")
    transport_cost: float = Field(..., alias="transportCost", description="Стоимость транспорта")
    delayed_delivery_discount_value: float = Field(..., alias="delayedDeliveryDiscountValue", description="Скидка за отложенную доставку")
    order_number: Optional[str] = Field(None, alias="orderNumber", description="Номер заказа")
    approvement_declined: bool = Field(..., alias="approvementDeclined", description="Согласование отклонено")
    available_for_distributor: bool = Field(..., alias="availableForDistributor", description="Доступно для дистрибьютора")
    client_brought_amount_result: float = Field(..., alias="clientBroughtAmountResult", description="Результат суммы клиента")
    is_end_user_pq: bool = Field(..., alias="isEndUserPQ", description="PQ конечного пользователя")
    auto_from_eng_spec: bool = Field(..., alias="autoFromEngSpec", description="Автоматически из инженерной спецификации")
    confirm_time_by_distr: Optional[datetime] = Field(None, alias="confirmTimeByDistr", description="Время подтверждения дистрибьютором")
    end_user_pq_status_id: Optional[UUID] = Field(None, alias="endUserPQStatusId", description="ID статуса PQ конечного пользователя")
    end_user_pq_description: Optional[str] = Field(None, alias="endUserPQDescription", description="Описание PQ конечного пользователя")
    response_time_client: Optional[datetime] = Field(None, alias="responseTimeClient", description="Время ответа клиента")
    passport_object: PassportObject = Field(..., alias="passportObject", description="Объект паспорта")
    status: OfferStatus = Field(..., description="Статус КП")
    eng_spec_type: Optional[EngSpecType] = Field(None, alias="engSpecType", description="Тип инженерной спецификации")
    purchase_type: PurchaseType = Field(..., alias="purchaseType", description="Тип покупки")
    distr_request: Optional[DistrRequest] = Field(None, alias="distrRequest", description="Запрос дистрибьютора")
    creator: Person = Field(..., description="Создатель")
    payment_term: PaymentTerm = Field(..., alias="paymentTerm", description="Условия оплаты")
    organization: Organization = Field(..., description="Организация")
    delivery: Delivery = Field(..., description="Доставка")
    one_c_current_status: Optional[str] = Field(None, alias="oneCCurrentStatus", description="Текущий статус в 1С")
    offer_type: OfferType = Field(..., alias="offerType", description="Тип КП")
    reservation_end: Optional[datetime] = Field(None, alias="reservationEnd", description="Окончание резервирования")
    complete_delivery_from: Optional[datetime] = Field(None, alias="completeDeliveryFrom", description="Полная доставка с")
    paid_storage: Optional[str] = Field(None, alias="paidStorage", description="Платное хранение")
    paid_storages: Optional[List[PaidStorage]] = Field(None, alias="paidStorages", description="Список платных хранилищ")
    delivery_options_xml: Optional[str] = Field(None, alias="deliveryOptionsXml", description="XML опций доставки")
    delivery_options_xml_dzr_prod: Optional[str] = Field(None, alias="deliveryOptionsXmlDZRProd", description="XML опций доставки DZR Prod")
    delivery_options_xml_prod: Optional[str] = Field(None, alias="deliveryOptionsXmlProd", description="XML опций доставки Prod")
    delivery_options_xml_hex: Optional[str] = Field(None, alias="deliveryOptionsXmlHex", description="XML опций доставки HEX")

    model_config = ConfigDict(
        alias_generator=lambda x: x[0].lower() + x[1:] if x else x,
    )


class Paging(BaseModel):
    page_number: int = Field(..., alias="pageNumber", description="Номер страницы")
    page_size: int = Field(..., alias="pageSize", description="Размер страницы")
    total_records: int = Field(..., alias="totalRecords", description="Общее количество записей")
    total_pages: int = Field(..., alias="totalPages", description="Общее количество страниц")

    model_config = ConfigDict(
        alias_generator=lambda x: x[0].lower() + x[1:] if x else x,
    )


class ResponseObject(BaseModel):
    errors: Optional[List[dict]] = Field(None, description="Список ошибок")
    offers: List[Offer] = Field(..., description="Список КП")
    paging: Optional[Paging] = Field(None, description="Информация о пагинации")

    model_config = ConfigDict(
        alias_generator=lambda x: x[0].lower() + x[1:] if x else x,
    )


class CommerceListModel(BaseModel):
    status: Status = Field(..., description="Статус ответа")
    messages: List[str] = Field(..., description="Список сообщений")
    objects: List[ResponseObject] = Field(..., description="Объекты ответа")

    model_config = ConfigDict(
        alias_generator=lambda x: x[0].lower() + x[1:] if x else x,
    )