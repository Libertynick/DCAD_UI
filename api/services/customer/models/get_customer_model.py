from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, field_validator, Field


class Signatories(BaseModel):
    personId: str = Field(description='id пользователя')
    signEndDate: Optional[datetime] = Field(description='Срок действия подписи.')
    isUnlimitedSigner: bool = Field(description='Бессрочная подпись')


class Contract(BaseModel):
    contractNumber: str = Field(description='Номер договора')
    contractEndDate: datetime = Field(description='Дата окончания договор')
    contractName: str = Field(description='Название договора')
    purchaserName: str = Field(description='Подписант договора')
    email: str = Field(description='Email организации')
    powerOfAttorneyBefore: Optional[datetime] = Field(description='Дата окончания действия доверенности')
    currency: str = Field(description='Валюта')


class PaymentTerm(BaseModel):
    code: str = Field(description='Код SAP')
    text: str = Field(description='Описание')
    creditDays: int = Field(description='Длительность кредита в днях')
    creditInterest: float = Field(description='Процент за кредит')
    conversionRate: float = Field(description='Процент за конвертацию')


class ResponsibleEngineer(BaseModel):
    name: str = Field(description='ФИО')
    personNumber: str = Field(description='Личный номер RUCO (0000xxxx)')
    salesGroup: str = Field(description='Allowed: RU1┃RU2┃RU4┃RU5┃RU7')
    phone: str = Field(description='Телефон')
    mail: str = Field(description='Адрес электронной почты')


class Address(BaseModel):
    zip: Optional[str] = Field(description='Почтовый индекс')
    country: Optional[str] = Field(description='Страна')
    city: Optional[str] = Field(description='Город')
    street: Optional[str] = Field(description='Улица')
    title: str = Field(description='Адрес целиком')


class Organization(BaseModel):
    contractorId: str = Field(description='Id организации')
    inn: str = Field(description='Инн организации')
    contractorName: str = Field(description='Название организации')


class Consignees(BaseModel):
    consigneeId: str = Field(description='ГрузополучательID')
    debtorId: str = Field(description='ГрузополучательID')
    contractId: str = Field(description='ID Договора')
    contractorName: str = Field(description='Наименование Контрагента')
    isPickup: bool = Field(description='Признак самовывозных условий')
    plant: Optional[str] = Field(description='Склад отгрузки')
    plantId: Optional[str] = Field(description='Код склада отгрузки')
    contractorInn: str = Field(description='ИНН Контрагента')
    debtorInn: Optional[str] = Field(description='ИНН Дебтора')
    fiasId: str = Field(description='Код Фиас')
    regionFiasId: Optional[str] = Field(description='Код фиас региона.')
    address: str = Field(description='Адрес Грузополучателя')
    sumOfDeliveryFrom: float = Field(description='Доставка, сумма от')
    currencyOfDeliverySum: str = Field(description='Валюта Allowed: RUB┃EUR┃CUCbr┃CU┃USD┃EUR5┃CNY')
    organizationShare: float = Field(description='Доставка, Доля Организации')
    contractorShare: float = Field(description='Доставка, Доля Контрагента')
    workingTime: str = Field(description='Время Работы')
    contractName: str = Field(description='Наименование договора')
    contractorCurrency: str = Field(description='Валюта Взаиморасчетов')
    contractStartDate: datetime = Field(description='Дата Начала Действия Договора')
    contractEndDate: datetime = Field(description='Дата Окончания Действия Договора')
    contacts: List[dict] = Field(annotated_types=List, description='Контактная Информация')


class Object(BaseModel):
    name: str = Field(description='Название клиента')
    inn: str = Field(description='ИНН')
    debtorAccount: str = Field(description='Клиентский номер')
    signatories: List[Signatories] = Field(description='Подписанты.')
    contract: Contract = Field(description='Модель договора.')
    customerHeadOffice: Optional[str] = Field(description='Головной офис')
    salesGroup: str = Field(description='Группа продажи')
    salesOffice: str = Field(description='Группа офиса')
    type: str = Field(description='Тип аккаунта')
    payTerms: str = Field(description='Условия оплаты')
    paymentTerms: List[PaymentTerm] = Field(description='Все условия оплаты из договора.')
    deliveryMode: Optional[str] = Field(description='Способ доставки')
    plant: Optional[str] = Field(description='Склад')
    orderBlockExt: Optional[str] = Field(description='Сообщение с блокировкой об отгрузке')
    deliverBlockExt: Optional[str] = Field(description='Сообщение с блокировкой о доставке')
    proformaBlockExt: Optional[str] = Field(description='ProformalBlockExt')
    blocked: bool = Field(
        description='Клиент заблокирован (см. коды блокировки OrderBlock, DeliveryBlock, ProformaBlock)')
    orderBlockLoc: Optional[str] = Field(description='')
    deliveryBlockLoc: Optional[str] = Field(description='')
    proformaBlockLoc: Optional[str] = Field(description='')
    responsibleEngineerNumber: str = Field(description='Номер ответственный инженер')
    responsibleEngineer: ResponsibleEngineer = Field(description='Сотрудник')
    partners: Optional[List[str]] = Field(description='Партнеры (не используется в Опене)')
    address: Address = Field(description='Модель адреса')
    contacts: Optional[str] = Field(description='Контакты клиента (не используется в Опене)')
    organization: Organization = Field(description='Продавец')
    statuses: Optional[str] = Field(description='Коллекция статусов Allowed: Ok┃Blocked')
    consignees: List[Consignees] = Field(description='Грузополучатели')

    # noinspection PyNestedDecorators

    @field_validator('name', 'inn', 'debtorAccount', 'signatories', 'payTerms', 'paymentTerms', 'consignees')
    @classmethod
    def fields_are_not_empty(cls, value, field_name):
        if len(value) == 0:
            field_name = field_name.field_name
            print(field_name, '-')
            raise ValueError(f'Поле {field_name} -  пустое!')
        else:
            return value


class GetCustomer(BaseModel):
    objects: List[Object] = []
    messages: list[str] = Field(description='Список сообщений или ошибок, возникших в процессе обработки запроса')
    status: str = Field(description='Статус ответа')
