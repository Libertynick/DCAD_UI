from datetime import datetime

from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel


class Status(str, Enum):
    OK = "Ok"
    WARNING = "Warning"
    ERROR = "Error"

    model_config = ConfigDict(
        use_enum_values=True
    )


class PurchaseType(BaseModel):
    """Информация о типе покупки."""
    id: UUID = Field(..., description='Идентификатор')
    value: Optional[str] = Field(None, description='Описание')
    allow_partial: bool = Field(..., description='')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class FileType(str, Enum):
    """Типы файлов."""
    SA = 'SA'
    SA5 = 'SA5'
    PO = 'PO'
    Default = 'Default'
    EndUserUPD = 'EndUserUPD'
    EndUserInvoice = 'EndUserInvoice'
    EndUserCommonFile = 'EndUserCommonFile'

    model_config = ConfigDict(
        use_enum_values=True
    )


class FileInfo(BaseModel):
    """Информация о файлах."""
    id: UUID = Field(..., description='')
    name: Optional[str] = Field(None, description='')
    create_date: Optional[datetime] = Field(None, description='Дата создания файла.')
    author: Optional[str] = Field(None, description='Имя автора файла.')
    file_type: FileType = Field(...,
                                description='Allowed: SA┃SA5┃PO┃Default┃EndUserUPD┃EndUserInvoice┃EndUserCommonFile')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class Currency(str, Enum):
    """Доступные валюты."""
    RUB = 'RUB'
    EUR = 'EUR'
    CUCbr = 'CUCbr'
    CU = 'CU'
    USD = 'USD'
    EUR5 = 'EUR5'
    CNY = 'CNY'

    model_config = ConfigDict(
        alias_generator=to_camel,
        use_enum_values=True

    )


class OrderStatus(BaseModel):
    """Информация о статусе заказа."""
    id: Optional[UUID] = Field(None, description='Идентификатор статуса (OneCRM)')
    display: Optional[str] = Field(None, description='Отображаемый статус')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class Organization(BaseModel):
    """Информация о продавце."""
    contractor_id: Optional[UUID] = Field(None, description='Идентификатор организации')
    inn: Optional[str] = Field(None, description='ИНН организации')
    contractor_name: Optional[str] = Field(None, description='Название организации')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class DocumentType(str, Enum):
    """Типы документов транзита."""
    Not = 'Not'
    OrderedByDistributor = 'OrderedByDistributor'
    OnTransitFromDistributor = 'OnTransitFromDistributor'
    Order = 'Order'
    PartR = 'PartR'

    model_config = ConfigDict(
        use_enum_values=True
    )


class TransitInfo(BaseModel):
    """Информация об ожидаемой поставке."""
    quantity: float = Field(..., description='Количество, зарезервированное в поставке для заказа')
    date: datetime = Field(..., description='Дата поступления на склад')
    document_type: DocumentType = Field(..., description='Тип документа транзита')
    document_number: Optional[str] = Field(None, description='Номер документа')
    document_date: Optional[datetime] = Field(None, description='Дата документа')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class OrderItem(BaseModel):
    """Информация о позиции заказа."""
    id: Optional[UUID] = Field(None, description='Идентификатор строки в OneCRM')
    text: Optional[str] = Field(None, description='Описание материала')
    code: Optional[str] = Field(None, description='Код материала')
    item: int = Field(..., description='Номер по-порядку')
    qty: float = Field(..., description='Количество')
    total_vat: float = Field(..., description='Итого с НДС')
    material_code: Optional[str] = Field(None, description='Код материала')
    available_for_order: float = Field(..., description='Доступно для заказа')
    delivered_count: int = Field(..., description='Количество доставленного')
    stock_count: int = Field(..., description='Количество зарезервированного на складе под заказ')
    packaged_count: int = Field(..., description='Количество упакованного')
    not_payed_count: int = Field(..., description='Сумма неоплаченного')
    transit: List[TransitInfo] = Field(..., description='Информация об ожидаемых поставках')
    shipped_at: Optional[datetime] = Field(None, description='Фактическая дата отгрузки со склада из 1С')
    is_canceled: bool = Field(..., description='Отменённая позиция')
    is_special_price: bool = Field(..., description='Применена ли специальная цена на позицию')
    odid: Optional[UUID] = Field(None, description='Идентификатор позиции в МКП')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class Order(BaseModel):
    """Информация о заказе."""
    base_offer_id: Optional[UUID] = Field(None, description='Базовое КП OneCRM')
    id: UUID = Field(..., description='Идентификатор OneCRM')
    create_date: datetime = Field(..., description='Дата создания')
    reservation_end: Optional[datetime] = Field(None, description='Окончание времени резервации')
    currency: Currency = Field(..., description='Валюта')
    currency_date: Optional[datetime] = Field(None, description='Дата курса валюты')
    euro_rate_offer: Optional[float] = Field(None, description='Курс евро')
    vat_result: float = Field(..., description='Сумма налога')
    va_tperc: float = Field(..., description='Процент налога')
    vat_coef: float = Field(..., description='Коэффициент налога (1+%/100)')
    surcharges_converstation: float = Field(..., description='Наценка за конвертацию')
    surcharges_payment: float = Field(..., description='Наценка за оплату')
    status: Optional[OrderStatus] = Field(None, description='Статус заказа')
    total: float = Field(..., description='Сумма')
    total_vat: float = Field(..., description='Сумма с налогами')
    total_distr_discount_price: float = Field(..., description='Сумма с учетом скидки дистрибьютора')
    reference_number: Optional[str] = Field(None, description='Ссылочный номер')
    document_number: Optional[str] = Field(None, description='Номер сбытового документа')
    created_at: datetime = Field(..., description='Дата создания')
    created_by: Optional[str] = Field(None, description='Создатель')
    payment_percent: float = Field(..., description='Оплачено, в % от суммы')
    items: List[OrderItem] = Field(..., description='Позиции заказа')
    organization: Organization = Field(..., description='Продавец')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class DeliveryTypeObject(BaseModel):
    """Информация о типе доставки."""
    id: UUID = Field(..., description='Идентификатор')
    value: Optional[str] = Field(None, description='Описание')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class DeliveryPayObject(BaseModel):
    """Информация об оплате доставки."""
    id: UUID = Field(..., description='Идентификатор')
    value: Optional[str] = Field(None, description='Описание')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class DeliveryTerms(BaseModel):
    """Информация об условиях доставки."""
    code: Optional[str] = Field(None, description='Код')
    debtor_account: Optional[str] = Field(None, description='Дебиторский счет')
    address: Optional[str] = Field(None, description='Адрес')
    company: Optional[str] = Field(None, description='Компания')
    city: Optional[str] = Field(None, description='Город')
    contact_person: Optional[str] = Field(None, description='Контактное лицо')
    instructions: Optional[str] = Field(None, description='Инструкции')
    source: Optional[str] = Field(None, description='Источник')
    delivery_type: Optional[str] = Field(None, description='Тип доставки')
    delivery_type_object: Optional[DeliveryTypeObject] = Field(None, description='Информация о типе доставки')
    delivery_pay: Optional[str] = Field(None, description='Оплата доставки')
    delivery_pay_object: Optional[DeliveryPayObject] = Field(None, description='Информация об оплате доставки')
    included: Optional[str] = Field(None, description='Включено')
    fias_id: Optional[str] = Field(None, description='ФИАС идентификатор')
    source_fias_id: Optional[str] = Field(None, description='ФИАС идентификатор источника')
    cost: Optional[str] = Field(None, description='Стоимость')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class PaymentTerm(BaseModel):
    """Информация об условиях оплаты."""
    code: Optional[str] = Field(None, description='Код')
    text: Optional[str] = Field(None, description='Текст')
    credit_days: Optional[int] = Field(None, description='Кредитные дни')
    prepay_percent: Optional[int] = Field(None, description='Процент предоплаты')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class DeliveryType(str, Enum):
    """Типы доставки."""
    Contract = 'Contract'
    ToAddress = 'ToAddress'
    FreeToAddress = 'FreeToAddress'
    Pickup = 'Pickup'
    PickupDZR = 'PickupDZR'

    model_config = ConfigDict(
        use_enum_values=True
    )


class MaterialType(str, Enum):
    """Типы кодов материалов."""
    regularCodesMSK = 'regularCodesMSK'
    regularCodesDZK = 'regularCodesDZK'
    productionCodesMSK = 'productionCodesMSK'
    productionCodesDZK = 'productionCodesDZK'

    model_config = ConfigDict(
        alias_generator=to_camel,
        use_enum_values=True
    )


class EndPoint(str, Enum):
    """Конечные точки доставки."""
    ToDoor = 'ToDoor'
    ToTK = 'ToTK'

    model_config = ConfigDict(
        use_enum_values=True
    )


class WrongDeliveryAddress(BaseModel):
    """Универсальный класс для описания адреса."""
    zip: Optional[str] = Field(None, description='Почтовый индекс')
    country: Optional[str] = Field(None, description='Страна')
    city: Optional[str] = Field(None, description='Город')
    street: Optional[str] = Field(None, description='Улица')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class ConsigneeContacts(BaseModel):
    """Контактные данные грузополучателя."""
    org_inn: Optional[str] = Field(None, description='ИНН организации')
    org_name: Optional[str] = Field(None, description='Название организации')
    person_name: Optional[str] = Field(None, description='Имя контактного лица')
    person_surname: Optional[str] = Field(None, description='Фамилия контактного лица')
    person_phone: Optional[str] = Field(None, description='Телефон контактного лица')
    person_additional_phone: Optional[str] = Field(None, description='Дополнительный телефон контактного лица')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class ConsigneeAgreementDelivery(BaseModel):
    """Согласованные параметры доставки."""
    source_fias_id: UUID = Field(..., description='ФИАС идентификатор откуда')
    destination_fias_id: Optional[UUID] = Field(None, description='ФИАС идентификатор куда')
    destination_region_fias_id: Optional[UUID] = Field(None, description='ФИАС идентификатор региона куда')
    address: Optional[str] = Field(None, description='Адрес назначения')
    paid_delivery: bool = Field(..., description='Платная доставка')
    condition_description: Optional[str] = Field(None, description='Полное описание условий доставки')
    inn: Optional[str] = Field(None, description='ИНН грузополучателя')
    kpp: Optional[str] = Field(None, description='КПП грузополучателя')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class ClientFinalDelivery(BaseModel):
    """Параметры доставки до конечного клиента."""
    source_fias_id: UUID = Field(..., description='ФИАС идентификатор откуда')
    destination_fias_id: Optional[UUID] = Field(None, description='ФИАС идентификатор куда')
    destination_region_fias_id: Optional[UUID] = Field(None, description='ФИАС идентификатор региона куда')
    address: Optional[str] = Field(None, description='Адрес назначения')
    paid_delivery: bool = Field(..., description='Платная доставка')
    wrong_delivery_address: Optional[WrongDeliveryAddress] = Field(None, description='Неверный адрес доставки')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class DeliveryOptions(BaseModel):
    """Параметры доставки при создании КП или Заказа."""

    consignee_code: Optional[str] = Field(None, description='Номер грузополучателя SAP')
    condition: Optional[str] = Field(None, description='Код способа доставки')
    mode: Optional[int] = Field(None, description='Тип доставки')
    delivery_type: DeliveryType = Field(..., description='Тип доставки')
    material_type: MaterialType = Field(..., description='Тип кода материала')
    delivery_cost: float = Field(..., description='Стоимость доставки')
    total_delivery_weight: Optional[float] = Field(None, description='Вес, для которого рассчитана стоимость')
    comment: Optional[str] = Field(None, description='Комментарий к параметрам доставки')
    consignee_agreement_delivery: ConsigneeAgreementDelivery = Field(...,
                                                                     description='Согласованные параметры доставки')
    client_final_delivery: Optional[ClientFinalDelivery] = Field(None,
                                                                 description='Параметры доставки до конечного клиента')
    consignee_contacts: Optional[ConsigneeContacts] = Field(None, description='Контактные данные грузополучателя')
    end_point: EndPoint = Field(..., description='Конечная точка доставки')
    desired_delivery_date: Optional[datetime] = Field(None, description='Желаемая дата отгрузки')
    deliver_full_set_only: bool = Field(..., description='Отгружать только при полной комплектации')
    cost_included_in_order: bool = Field(..., description='Стоимость доставки включена в заказ')
    consignee_id: Optional[UUID] = Field(None, description='Идентификатор грузополучателя')

    model_config = ConfigDict(
        alias_generator=to_camel,
        use_enum_values=True
    )


class DeliveryOptionsDzrProd(BaseModel):
    """Параметры доставки при создании КП или Заказа. ПТО"""

    consignee_code: Optional[str] = Field(None, description='Номер грузополучателя SAP')
    condition: Optional[str] = Field(None, description='Код способа доставки')
    mode: Optional[int] = Field(None, description='Тип доставки')
    delivery_type: DeliveryType = Field(..., description='Тип доставки')
    material_type: MaterialType = Field(..., description='Тип кода материала')
    delivery_cost: float = Field(..., description='Стоимость доставки')
    total_delivery_weight: Optional[float] = Field(None, description='Вес, для которого рассчитана стоимость')
    comment: Optional[str] = Field(None, description='Комментарий к параметрам доставки')
    consignee_agreement_delivery: ConsigneeAgreementDelivery = Field(...,
                                                                     description='Согласованные параметры доставки')
    client_final_delivery: Optional[ClientFinalDelivery] = Field(None,
                                                                 description='Параметры доставки до конечного клиента')
    consignee_contacts: Optional[ConsigneeContacts] = Field(None, description='Контактные данные грузополучателя')
    end_point: EndPoint = Field(..., description='Конечная точка доставки')
    desired_delivery_date: Optional[datetime] = Field(None, description='Желаемая дата отгрузки')
    deliver_full_set_only: bool = Field(..., description='Отгружать только при полной комплектации')
    cost_included_in_order: bool = Field(..., description='Стоимость доставки включена в заказ')
    consignee_id: Optional[UUID] = Field(None, description='Идентификатор грузополучателя')

    model_config = ConfigDict(
        alias_generator=to_camel,
        use_enum_values=True
    )


class DeliveryOptionsProd(BaseModel):
    """Параметры доставки при создании КП или Заказа. Шкафы БАСТ"""

    consignee_code: Optional[str] = Field(None, description='Номер грузополучателя SAP')
    condition: Optional[str] = Field(None, description='Код способа доставки')
    mode: Optional[int] = Field(None, description='Тип доставки')
    delivery_type: DeliveryType = Field(..., description='Тип доставки')
    material_type: MaterialType = Field(..., description='Тип кода материала')
    delivery_cost: float = Field(..., description='Стоимость доставки')
    total_delivery_weight: Optional[float] = Field(None, description='Вес, для которого рассчитана стоимость')
    comment: Optional[str] = Field(None, description='Комментарий к параметрам доставки')
    consignee_agreement_delivery: ConsigneeAgreementDelivery = Field(...,
                                                                     description='Согласованные параметры доставки')
    client_final_delivery: Optional[ClientFinalDelivery] = Field(None,
                                                                 description='Параметры доставки до конечного клиента')
    consignee_contacts: Optional[ConsigneeContacts] = Field(None, description='Контактные данные грузополучателя')
    end_point: EndPoint = Field(..., description='Конечная точка доставки')
    desired_delivery_date: Optional[datetime] = Field(None, description='Желаемая дата отгрузки')
    deliver_full_set_only: bool = Field(..., description='Отгружать только при полной комплектации')
    cost_included_in_order: bool = Field(..., description='Стоимость доставки включена в заказ')
    consignee_id: Optional[UUID] = Field(None, description='Идентификатор грузополучателя')

    model_config = ConfigDict(
        alias_generator=to_camel,
        use_enum_values=True
    )


class DeliveryOptionsHex(BaseModel):
    """Параметры доставки при создании КП или Заказа. Зип и изоляция"""

    consignee_code: Optional[str] = Field(None, description='Номер грузополучателя SAP')
    condition: Optional[str] = Field(None, description='Код способа доставки')
    mode: Optional[int] = Field(None, description='Тип доставки')
    delivery_type: DeliveryType = Field(..., description='Тип доставки')
    material_type: MaterialType = Field(..., description='Тип кода материала')
    delivery_cost: float = Field(..., description='Стоимость доставки')
    total_delivery_weight: Optional[float] = Field(None, description='Вес, для которого рассчитана стоимость')
    comment: Optional[str] = Field(None, description='Комментарий к параметрам доставки')
    consignee_agreement_delivery: ConsigneeAgreementDelivery = Field(...,
                                                                     description='Согласованные параметры доставки')
    client_final_delivery: Optional[ClientFinalDelivery] = Field(None,
                                                                 description='Параметры доставки до конечного клиента')
    consignee_contacts: Optional[ConsigneeContacts] = Field(None, description='Контактные данные грузополучателя')
    end_point: EndPoint = Field(..., description='Конечная точка доставки')
    desired_delivery_date: Optional[datetime] = Field(None, description='Желаемая дата отгрузки')
    deliver_full_set_only: bool = Field(..., description='Отгружать только при полной комплектации')
    cost_included_in_order: bool = Field(..., description='Стоимость доставки включена в заказ')
    consignee_id: Optional[UUID] = Field(None, description='Идентификатор грузополучателя')

    model_config = ConfigDict(
        alias_generator=to_camel,
        use_enum_values=True
    )


class DistrApprovement(BaseModel):
    """Информация об одобрении дистрибьютором."""
    person_id: Optional[UUID] = Field(None, description='Идентификатор лица')
    email: Optional[str] = Field(None, description='Email')
    phone: Optional[str] = Field(None, description='Телефон')
    name: Optional[str] = Field(None, description='Имя')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class EndClientOrderCreator(BaseModel):
    """Информация о создателе заказа конечного клиента."""
    person_id: Optional[UUID] = Field(None, description='Идентификатор лица')
    email: Optional[str] = Field(None, description='Email')
    phone: Optional[str] = Field(None, description='Телефон')
    name: Optional[str] = Field(None, description='Имя')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class Comment(BaseModel):
    """Комментарии клиента и дистрибьютора."""
    comment: Optional[str] = Field(None, description='Комментарий')
    author: Optional[str] = Field(None, description='Автор комментария')
    create_date: Optional[datetime] = Field(None, description='Время создания комментария')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class OfferType(str, Enum):
    """Типы создаваемых КП."""
    PQ = 'PQ'
    HR = 'HR'
    CLH = 'CLH'
    IND = 'IND'
    BTP = 'BTP'

    model_config = ConfigDict(
        alias_generator=to_camel,
        use_enum_values=True
    )


class Source(str, Enum):
    """Источники создания заказа."""
    CRM = 'CRM'
    CSD = 'CSD'
    WebClient = 'WebClient'

    model_config = ConfigDict(
        use_enum_values=True
    )


class Data(BaseModel):
    """Информация о КП/Заказе."""
    delayed_delivery_discount_value: Optional[float] = Field(
        None, description='Скидка за поставку под заказ. Сумма в валюте заказа')
    purchase_type: Optional[PurchaseType] = Field(None, description='Тип покупки')
    pay_percent_before_placing_into_production: Optional[int] = Field(None,
                                                                      description='Процент предоплаты перед отгрузкой')
    files_po: Optional[List[FileInfo]] = Field(None, description='Файлы заказа')
    files_sa5: Optional[List[FileInfo]] = Field(None, description='Файлы SA5')
    files_sa: Optional[List[FileInfo]] = Field(None, description='Файлы SA')
    files: Optional[List[FileInfo]] = Field(None, description='Общий список файлов')
    term_date: Optional[datetime] = Field(None, description='Планируемая дата отгрузки')
    sap_author_person_number: Optional[str] = Field(None, description='Номер автора в системе SAP')
    sap_code_delivery: Optional[str] = Field(None, description='Код доставки в системе SAP')
    crm_passport_number: Optional[int] = Field(None, description='Номер паспорта в CRM')
    passport_id: Optional[UUID] = Field(None, description='Идентификатор паспорта')
    passport_responsible_phone: Optional[str] = Field(None, description='Телефон ответственного за паспорт')
    passport_responsible_name: Optional[str] = Field(None, description='Имя ответственного за паспорт')
    passport_responsible_email: Optional[str] = Field(None, description='Email ответственного за паспорт')
    passport_responsible_number: Optional[str] = Field(None, description='Номер ответственного за паспорт')
    specification_title: Optional[str] = Field(None, description='Заголовок спецификации')
    markup_percent_result: Optional[float] = Field(None, description='Процент наценки')
    markup_result: Optional[float] = Field(None, description='Результирующая наценка')
    euro_rate_offer: Optional[float] = Field(None, description='Курс евро для оферты')
    client_brought_amount_result: float = Field(..., description='Сумма, внесённая клиентом')
    currency_date: datetime = Field(..., description='Дата курса')
    sync_date: Optional[datetime] = Field(None, description='Дата последней синхронизации заказа с учетной системой')
    currency: Currency = Field(..., description='Валюта')
    vat_coef: Optional[float] = Field(None, description='Коэффициент НДС')
    va_tperc: int = Field(..., description='Процент НДС')
    is_end_user_p_q: bool = Field(..., description='Заказ конечного покупателя')
    vat_result: Optional[float] = Field(None, description='Сумма НДС')
    total_vat: Optional[float] = Field(None, description='Сумма с НДС')
    total: Optional[float] = Field(None, description='Сумма без НДС')
    valid_date: datetime = Field(..., description='До какого дня акруально КП')
    valid_days: Optional[int] = Field(None, description='Количество дней актуальности КП')
    total_distr_discount_price: Optional[float] = Field(None, description='Общая сумма c учетом скидки дистрибьютора')
    sales_price: Optional[float] = Field(None, description='Цена продажи')
    object_city: Optional[str] = Field(None, description='Город объекта')
    object_address: Optional[str] = Field(None, description='Адрес объекта')
    object_number: Optional[int] = Field(None, description='Номер объекта')
    object_name: Optional[str] = Field(None, description='Название объекта')
    orders: Optional[List[Order]] = Field(None, description='Список заказов')
    debtor_account: Optional[str] = Field(None, description='Лицевой счет дебитора')
    payer_display: Optional[str] = Field(None, description='Наименование плательщика')
    payer_id: UUID = Field(..., description='Идентификатор плательщика')
    payment_term: Optional[PaymentTerm] = Field(None, description='Условия оплаты')
    end_user_client: Optional[str] = Field(None, description='Наименование конечного клиента')
    create_date: datetime = Field(..., description='Дата создания')
    commerce_number: Optional[str] = Field(None, description='Коммерческий номер')
    delivery_short_info: Optional[str] = Field(None, description='Краткая информация о доставке')
    delivery_condition: Optional[str] = Field(None, description='Условия доставки')
    status_display: Optional[str] = Field(None, description='Статус')
    status: UUID = Field(..., description='Идентификатор статуса')
    surcharges_payment: float = Field(..., description='Наценка за оплату')
    surcharges_convertation: float = Field(..., description='Наценка за конвертацию')
    partial_purchase: Optional[bool] = Field(None, description='Частичная закупка')
    crm_commerce_id: UUID = Field(..., description='Идентификатор сделки в CRM')
    sales_office: Optional[str] = Field(None, description='Офис продаж')
    final_client_inn: Optional[str] = Field(None, description='ИНН конечного клиента')
    payer_inn: Optional[str] = Field(None, description='ИНН плательщика')
    delivery_options: Optional[DeliveryOptions] = Field(None,
                                                        description='Параметры доставки при создании КП или Заказа')
    delivery_options_hex: Optional[DeliveryOptionsHex] = Field(None,
                                                            description='Параметры доставки при создании КП или Заказа')
    delivery_options_prod: Optional[DeliveryOptionsProd] = Field(None,
                                                                 description='Параметры доставки при создании КП или Заказа')
    delivery_options_d_z_r_prod: Optional[DeliveryOptionsDzrProd] = Field(None,
                                                                          description='Параметры доставки при создании КП или Заказа. ПТО')
    available_for_distributor: bool = Field(..., description='Доступность для дистрибьютора')
    is_order: bool = Field(..., description='Является ли заказом')
    is_valid: bool = Field(..., description='Является ли заказ действительным')
    is_i_t_psuccess: bool = Field(..., description='Успешность ITPS')
    creator_user_id: UUID = Field(..., description='Идентификатор создателя')
    creator_person_id: Optional[UUID] = Field(None, description='Идентификатор человека, создавшего заказ')
    creator_display: Optional[str] = Field(None, description='Отображаемое имя создателя')
    order_number: Optional[str] = Field(None, description='Номер заказа')
    sap_reference_number: Optional[str] = Field(None, description='Референсный номер в SAP')
    approvement_declined: bool = Field(..., description='Одобрение отклонено')
    distr_approvement: Optional[DistrApprovement] = Field(None, description='Информация об одобрении дистрибьютором')
    end_client_order_creator: Optional[EndClientOrderCreator] = Field(None,
                                                                      description='Информация о создателе заказа конечного клиента')
    auto_distr_discount: Optional[float] = Field(None, description='Скидка дистрибьютора (авторасчет)')
    final_bayer_id: Optional[UUID] = Field(None, description='Идентификатор конечного покупателя')
    is_pinned_final_buyer: Optional[bool] = Field(None, description='Закреплен ли конечный покупатель')
    reservation_end: Optional[datetime] = Field(None, description='Окончание времени резервации')
    auto_client_discount: Optional[float] = Field(None, description='Скидка клиента (авторасчет)')
    comments: Optional[List[Comment]] = Field(None, description='Комментарии клиента и дистрибьютора')
    end_user_pq_status_id: Optional[UUID] = Field(None, description='Статус заказа конечного клиента')
    end_user_pq_description: Optional[str] = Field(None, description='Описание статуса заказа конечного клиента')
    confirm_time_by_distr: Optional[datetime] = Field(None,
                                                      description='Время не позднее которого дистр должен принять КП')
    response_time_client: Optional[datetime] = Field(None,
                                                     description='Время не позднее которого конечный клиент должен принять КП')
    opportunity_id: Optional[UUID] = Field(None, description='Идентификатор сделки OneCRM, в которой создаётся заказ')
    final_buyer_cdl_id: Optional[UUID] = Field(None, description='Идентификатор договора конечника')
    offer_type: OfferType = Field(..., description='Тип создаваемого КП')
    show_price_with_discount: Optional[bool] = Field(None, description='Показывать цену со скидкой в прайсе')
    source: Optional[Source] = Field(None, description='Источник создания заказа')
    one_c_current_status: Optional[str] = Field(None, description='Текущий статус заказа в 1С')
    client_person_id: Optional[UUID] = Field(None,
                                             description='Идентификатор логина сотрудника конечного клиента для РОЛ КП')
    delivery_terms: Optional[List[DeliveryTerms]] = Field(None, description='Условия доставки')
    delivery_terms_pto: Optional[List[DeliveryTerms]] = Field(None, description='Условия доставки для ПТО')

    model_config = ConfigDict(
        alias_generator=to_camel,
        use_enum_values=True
    )


class LineType(str, Enum):
    """Виды позиций."""
    Material = 'Material'
    HEX = 'HEX'
    BTP = 'BTP'
    HEXAdditions = 'HEXAdditions'
    AutoShield = 'AutoShield'
    TDU = 'TDU'
    Pump = 'Pump'
    UNKNOWN = 'UNKNOWN'

    model_config = ConfigDict(
        alias_generator=to_camel,
        use_enum_values=True
    )


class BomSetItem(BaseModel):
    """Информация о позиции в комплекте."""
    material_code: Optional[str] = Field(None, description='Код материала')
    material_description: Optional[str] = Field(None, description='Описание позиции комплекта')
    quantity: float = Field(..., description='Количество в позиции в комплекте')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class AppliedPromo(BaseModel):
    """Информация о примененной промо-акции."""
    currency_value: float = Field(..., description='Промо курс')
    name: Optional[str] = Field(None, description='Название промо')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class Details(BaseModel):
    from_moscow: bool = Field(..., description='Из Москвы')
    weight: Optional[float] = Field(None, description='Вес')
    package_size: int = Field(..., description='Размер упаковки')
    pto_ready_for_shipment_value: Optional[int] = Field(None, description='DEPRECATED')
    isl_box: bool = Field(..., description='DEPRECATED')
    is_b_t_p: bool = Field(..., description='DEPRECATED')
    is_p_t_o: bool = Field(..., description='DEPRECATED')
    is_t_d_u: bool = Field(..., description='DEPRECATED')
    line_type: LineType = Field(
        ..., description='Вид позиции Allowed: Material┃HEX┃BTP┃HEXAdditions┃AutoShield┃TDU┃Pump┃UNKNOWN')
    markup_percent_result: Optional[float] = Field(None, description='Результат наценки в процентах')
    markup_result: Optional[float] = Field(None, description='Результат наценки')
    price_group: Optional[str] = Field(None, description='Ценовая группа')
    total_vat: Optional[float] = Field(None, description='Итого с НДС')
    total: float = Field(..., description='Общая сумма')
    vat_result: Optional[float] = Field(None, description='Сумма НДС')
    retail_price_result_no_n_d_s: float = Field(..., description='Розничная цена по прайсу без НДС')
    retail_price_result: float = Field(..., description='Розничная цена по прайсу с НДС')
    discount: Optional[float] = Field(None, description='Скидка')
    currency: Currency = Field(..., description='Валюта')
    sales_price: Optional[float] = Field(None, description='Цена продажи')
    client_sales_price: Optional[float] = Field(None, description='Цена клиента')
    text: Optional[str] = Field(None, description='Описание')
    code: Optional[str] = Field(None, description='Код материала')
    material_code: Optional[str] = Field(None, description='Код материала из ассортимента')
    qty: float = Field(..., description='Количество')
    id: Optional[UUID] = Field(None, description='Идентификатор')
    item: int = Field(..., description='Номер по-порядку')
    hex_number: Optional[str] = Field(None, description='Номер НЕХ')
    btp_number: Optional[str] = Field(None, description='Номер BTP')
    warranty_total: Optional[float] = Field(None, description='Гарантия, Итого')
    client_discount_percent: Optional[float] = Field(None, description='Скидка клиента, процент')
    client_brought_amount_result: Optional[float] = Field(None, description='Итого клиента с НДС')
    available_for_order: float = Field(..., description='Доступно для заказа')
    delivered_count: int = Field(..., description='Количество доставленного')
    stock_count: int = Field(..., description='Количество зарезервированного на складе под заказ')
    packaged_count: int = Field(..., description='Количество упакованного')
    not_payed_count: int = Field(..., description='Сумма неоплаченного')
    transit: Optional[List[TransitInfo]] = Field(None, description='Информация об ожидаемых поставках')
    is_canceled: bool = Field(..., description='Целиком отменённая позиция')
    canceled_quantity: int = Field(..., description='Отменённая позиция')
    cancel_reason: Optional[str] = Field(None, description='Причина отмены позиции')
    is_special_price: bool = Field(..., description='Применена ли специальная цена на позицию')
    bom_set: Optional[List[BomSetItem]] = Field(None, description='Состав комплекта')
    organization: Organization = Field(..., description='Продавец')
    shipped_at: Optional[datetime] = Field(None, description='Фактическая дата отгрузки со склада из 1С')
    applied_promo: Optional[AppliedPromo] = Field(None, description='Примененная промо-акция')
    invoice_number: Optional[str] = Field(None, description='Номер документа об отгрузке')
    invoice_date: Optional[datetime] = Field(None, description='Дата УПД')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class Permissions(BaseModel):
    edit: bool = Field(..., description='Редактирование заказа')
    move_to_draft: bool = Field(..., description='Перемещение в черновики')
    delete: bool = Field(..., description='Удаление заказа')
    add_comment: bool = Field(..., description='Добавление комментария')
    add_file: bool = Field(..., description='Добавление файла')
    get_file: bool = Field(..., description='Получение файла')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class ResponseObject(BaseModel):
    data: List[Data] = Field(..., description='Информация о КП/Заказе')
    details: List[Details] = Field(..., description='Список позиций КП/заказа')
    permissions: Permissions = Field(..., description='')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class ModelFullCommerceNew(BaseModel):
    status: Status = Field(..., description="Статус ответа")
    messages: List[str] = Field(..., description="Список сообщений или ошибок, возникших в процессе обработки запроса")
    objects: List[ResponseObject] = Field(..., description="Ответ с результатом создания заказа")
