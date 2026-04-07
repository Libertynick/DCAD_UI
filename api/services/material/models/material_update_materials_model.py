from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import List

from pydantic.alias_generators import to_camel


class StatusEnum(str, Enum):
    Ok = "Ok"
    Warning = "Warning"
    Error = "Error"


class UpdateMaterialModel(BaseModel):
    status: StatusEnum = Field(..., description="Статус ответа: Ok, Warning или Error")
    messages: List[str] = Field(..., description="Список сообщений или ошибок, возникших в процессе обработки запроса")
    objects: List[bool] = Field(..., description="Ответ в виде списка логических значений")

    model_config = ConfigDict(
        alias_generator=to_camel,
        use_enum_values=True
    )
