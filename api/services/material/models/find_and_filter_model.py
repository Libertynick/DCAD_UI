from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel


class StatusEnum(str, Enum):
    OK = "Ok"
    WARNING = "Warning"
    ERROR = "Error"

    model_config = ConfigDict(
        use_enum_values=True
    )


class DocumentTypeEnum(str, Enum):
    REPLACEMENT_LETTER = "Письмо о замене"
    PASSPORT = "Паспорт"
    USER_MANUAL = "Руководство по эксплуатации"
    TECHNICAL_DESCRIPTION = "Техническое описание"
    CERTIFICATE = "Сертификат"
    PHOTO = "Фото"
    CATALOG = "Каталог"

    model_config = ConfigDict(
        use_enum_values=True
    )


class Document(BaseModel):
    type: str = Field(..., description='Тип документа')
    document_number: Optional[str] = Field(None, description='Номер документа')
    doc_set_number: Optional[str] = Field(None, description='Номер набора документов')
    doc_version: Optional[str] = Field(None, description='Версия документа')
    doc_revision: Optional[str] = Field(None, description='Ревизия документа')
    local_title: Optional[str] = Field(None, description='Локальное название')
    legacy_literature_number: Optional[str] = Field(None, description='Номер литературы (legacy)')
    status: Optional[str] = Field(None, description='Статус документа')
    file_extension: str = Field(..., description='Расширение файла')
    type_number: int = Field(..., description='Номер типа')
    display_name: Optional[str] = Field(None, description='Отображаемое имя')
    id: Optional[str] = Field(None, description='Идентификатор документа')
    title: Optional[str] = Field(None, description='Название документа')
    created: datetime = Field(..., description='Дата создания')
    modified: datetime = Field(..., description='Дата изменения')
    updated: datetime = Field(..., description='Дата обновления')
    file_size_in_bytes: int = Field(..., description='Размер файла в байтах')
    public_file_url: str = Field(..., description='Публичный URL файла')
    is_archive: bool = Field(..., description='Является ли архивом')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class AreaActivity(BaseModel):
    id: UUID = Field(..., description='Идентификатор области активности')
    description: str = Field(..., description='Описание области активности')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class Gfu(BaseModel):
    id: UUID = Field(..., description='Идентификатор GFU')
    description: str = Field(..., description='Описание GFU')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class MaterialObject(BaseModel):
    id: int = Field(..., description='Идентификатор материала')
    code: str = Field(..., description='Код материала')
    alt_code: str = Field(..., description='Альтернативный код')
    ekgrp: Optional[str] = Field(None, description='Группа закупок')
    description: str = Field(..., description='Описание материала')
    description_ext: Optional[str] = Field(None, description='Расширенное описание')
    info: str = Field(..., description='Информация')
    sales_price: float = Field(..., description='Цена продажи')
    delivery_time_standard: str = Field(..., description='Стандартное время доставки')
    pack_size: int = Field(..., description='Размер упаковки')
    price_group: Optional[str] = Field(None, description='Ценовая группа')
    comm_code: Optional[str] = Field(None, description='Коммерческий код')
    line_type: str = Field(..., description='Тип линии')
    promo_currency_value: Optional[int] = Field(None, description='Значение валюты промо')
    promo_expired_date: Optional[datetime] = Field(None, description='Дата окончания промо')
    net_weight: float = Field(..., description='Чистый вес')
    gross_weight: Optional[float] = Field(None, description='Общий вес')
    currency: str = Field(..., description='Валюта')
    characteristics: List = Field(default=[], description='Характеристики')
    documents: List[Document] = Field(default=[], description='Список документов')
    images: List = Field(default=[], description='Изображения')
    statuses: List = Field(default=[], description='Статусы')
    bom_material_codes: List = Field(default=[], description='Коды BOM материалов')
    segments: List[str] = Field(default=[], description='Сегменты')
    equipment_category_id: Optional[UUID] = Field(None, description='Идентификатор категории оборудования')
    mpg: Optional[str] = Field(None, description='MPG')
    area_activity: Optional[AreaActivity] = Field(None, description='Область активности')
    gfu: Optional[Gfu] = Field(None, description='GFU')
    related_products: Optional[str] = Field(None, description='Связанные продукты')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )


class FindAndFilterModel(BaseModel):
    status: StatusEnum = Field(..., description='Статус ответа')
    messages: List[str] = Field(default=[], description='Список сообщений или ошибок')
    objects: List[MaterialObject] = Field(default=[], description='Список объектов материалов')

    model_config = ConfigDict(
        alias_generator=to_camel,
    )