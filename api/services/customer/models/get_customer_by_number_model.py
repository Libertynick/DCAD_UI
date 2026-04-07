from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, StrictStr, field_validator


class Contact(BaseModel):
    contactType: Optional[str] = Field(description="Тип контакта")
    value: Optional[str] = Field(description="Значение контакта")


class Employee(BaseModel):
    name: Optional[str] = Field(description="Имя сотрудника")
    contactInformation: List[Contact] = Field(description="Контактная информация сотрудника")


class Contract(BaseModel):
    id: UUID = Field(description="Идентификатор договора")
    contractName: Optional[str] = Field(description="Название договора")
    startDate: datetime = Field(description="Дата начала договора")
    endDate: datetime = Field(description="Дата окончания договора")
    organizationName: Optional[str] = Field(description="Название организации")
    organizationINN: Optional[str] = Field(description="ИНН организации")
    salesDepartmentCode: Optional[str] = Field(description="Код отдела продаж")
    salesDepartmentName: Optional[str] = Field(description="Название отдела продаж")
    salesDepartmentId: Optional[str] = Field(description="Идентификатор отдела продаж")
    contragentId: Optional[str] = Field(description="Идентификатор контрагента")


class Object(BaseModel):
    id: UUID = Field(description="Идентификатор объекта")
    privateName: Optional[str] = Field(description="Частное название объекта")
    publicName: Optional[str] = Field(description="Публичное название объекта")
    inn: Optional[str] = Field(description="ИНН объекта")
    sendUtdViaProvider: bool = Field(description="Флаг отправки УТД через провайдера")
    printUtd: bool = Field(description="Флаг печати УТД")
    contragentType: Optional[str] = Field(description="Тип контрагента")
    contacts: List[Contact] = Field(description="Контакты объекта")
    debtorAccount: Optional[str] = Field(description="Дебиторский счет объекта")
    contracts: List[Contract] = Field(description="Договоры объекта")
    employees: List[Employee] = Field(description="Сотрудники объекта")
    region: Optional[str] = Field(description="Регион объекта")
    regionFiasId: Optional[str] = Field(description="Идентификатор региона по ФИАС")

    # noinspection PyNestedDecorators
    @field_validator('publicName', 'inn', 'contacts', 'debtorAccount')
    @classmethod
    def fields_are_not_empty(cls, value, field_name):
        if len(value) == 0:
            field_name = field_name.field_name
            print(field_name, '-')
            raise ValueError(f'Поле {field_name} -  пустое!')
        else:
            return value


class GetCustomerByNumber(BaseModel):
    status: StrictStr = Field(description="Статус ответа", choices=["Ok", "Warning", "Error"])
    messages: List[str] = Field(description="Список сообщений или ошибок")
    objects: List[Object] = Field(description="Объекты ответа")
