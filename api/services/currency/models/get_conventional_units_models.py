from enum import Enum
from typing import List

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class Status(str, Enum):
    ok = 'Ok'
    warning = 'Warning'
    error = 'Error'

    model_config = ConfigDict(
        alias_generator=to_camel,
        use_enum_values=True,

    )


class GetConventionalUnitsModel(BaseModel):
    status: Status = Field(description='Статус ответа Allowed: Ok┃Warning┃Error')
    objects: List[float] = Field(description='Ответ')
