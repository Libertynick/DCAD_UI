from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


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


class Characteristic(BaseModel):
    """
    Модель характеристики материала.

    Attributes:
    - name (str): Название характеристики.
    - value (str): Значение характеристики.
    """
    name: Optional[str] = Field(None, description='Название характеристики')
    value: Optional[str] = Field(None, description='Значение характеристики')


class Material(BaseModel):
    """
    Модель материала.

    Attributes:
    - id (int): ID материала.
    - code (str): Код материала.
    - altCode (str): Альтернативный код материала.
    - description (str): Описание материала.
    - descriptionExt (str): Расширенное описание материала.
    - info (str): Дополнительная информация.
    - characteristics (List[Characteristic]): Список характеристик материала.
    """
    id: Optional[int] = Field(None, description='ID материала')
    code: Optional[str] = Field(None, description='Код материала')
    altCode: Optional[str] = Field(None, alias='altCode', description='Альтернативный код материала')
    description: Optional[str] = Field(None, description='Описание материала')
    descriptionExt: Optional[str] = Field(None, alias='descriptionExt', description='Расширенное описание материала')
    info: Optional[str] = Field(None, description='Дополнительная информация')
    characteristics: List[Characteristic] = Field(default=[], description='Список характеристик материала')


class AnalogObject(BaseModel):
    """
    Модель объекта аналога.

    Attributes:
    - id (int): ID записи.
    - material (Material): Исходный материал.
    - analogMaterial (Material): Материал-аналог.
    - comment (str): Комментарий.
    """
    id: Optional[int] = Field(None, description='ID записи')
    material: Optional[Material] = Field(None, description='Исходный материал')
    analogMaterial: Optional[Material] = Field(None, alias='analogMaterial', description='Материал-аналог')
    comment: Optional[str] = Field(None, description='Комментарий')


class FindAnalogsModel(BaseModel):
    """
    Основная модель для описания формата ответа API FindAnalogs.

    Attributes:
    - status (StatusEnum): Статус ответа, указывающий на результат обработки запроса.
    - messages (List[str]): Список сообщений или ошибок, возникших в процессе обработки запроса.
    - objects (List[AnalogObject]): Список объектов с информацией об аналогах материалов.
    """
    status: StatusEnum = Field(..., description='Статус ответа')
    messages: List[str] = Field(default=[], description='Список сообщений или ошибок')
    objects: List[AnalogObject] = Field(default=[], description='Список объектов с информацией об аналогах материалов')