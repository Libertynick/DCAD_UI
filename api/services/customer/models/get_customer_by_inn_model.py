from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime


class Contact(BaseModel):
    contactType: Optional[str]
    value: Optional[str]


class Contract(BaseModel):
    id: str  # добавить описание полей
    contractName: Optional[str]
    startDate: datetime
    endDate: datetime
    organizationName: Optional[str]
    organizationINN: Optional[str]
    salesDepartmentCode: Optional[str]
    salesDepartmentName: Optional[str]
    salesDepartmentId: Optional[str]
    contragentId: Optional[str]


class ContactInformation(BaseModel):
    contactType: Optional[str]


class Employees(BaseModel):
    name: Optional[str]
    contactInformation: List[ContactInformation]
    value: Optional[str]


class Object(BaseModel):
    id: str
    privateName: Optional[str]
    publicName: Optional[str]
    inn: Optional[str]
    sendUtdViaProvider: bool
    printUtd: bool
    contragentType: Optional[str]
    contacts: Optional[List[Contact]] = None
    debtorAccount: Optional[str]
    contracts: List[Contract]
    region: Optional[str]
    regionFiasId: Optional[str]

    # noinspection PyNestedDecorators
    # @field_validator('publicName', 'inn', 'contacts', 'debtorAccount')
    # @classmethod
    # def fields_are_not_empty(cls, value, field_name):
    #     print(value, '\n')
    #     if len(value) == 0:
    #         field_name = field_name.field_name
    #         print(field_name, '-')
    #         raise ValueError(f'Поле {field_name} -  пустое!')
    #     else:
    #         return value


class GetCustomerByInn(BaseModel):
    objects: List[Object]
    messages: List[str]
    status: str
