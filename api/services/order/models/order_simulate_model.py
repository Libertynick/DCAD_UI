from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel


class ScheduleType(str, Enum):
    stock = "Stock"
    transit = "Transit"
    unavailable = "Unavailable"
    manufacturing = "Manufacturing"

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class Schedules(BaseModel):
    line_number: int = Field(description='Номер позиции в расчете')
    confirmed_quantity: int = Field(
        description='Подтвержденное количество: на складе, в пути, недоступное, в зависимости от статуса наличия')
    corrected_quantity: int = Field(description='Исправленное количество (в случае продажи материала только упаковкой')
    ordered_quantity: int = Field(description='Заказанное количество')
    delivery_date: Optional[datetime] = Field(description='Дата поставки, м.б. пустой в зависимости от статуса наличия')
    corrected_delivery_date: Optional[str] = Field(
        description='Скорректированная дата поставки, м.б. пустой в зависимости от статуса наличия')
    schedule_type: ScheduleType = Field(description='Виды статусов наличия')

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class Currency(str, Enum):
    rub = "RUB"
    eur = "EUR"
    cu_cbr = "CUCbr"
    cu = "CU"
    usd = "USD"
    eur_5 = "EUR5"
    cny = "CNY"

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        use_enum_values=True
    )


class CostCurrency(str, Enum):
    rub = "RUB"
    eur = "EUR"
    cu_cbr = "CUCbr"
    cu = "CU"
    usd = "USD"
    eur_5 = "EUR5"
    cny = "CNY"

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class Comments(BaseModel):
    comment: Optional[str] = Field(description='Текст комментария')
    color: Optional[str] = Field(description='Цвет текста комментария (red, blue и т.п.)')


class Statuses(BaseModel):
    code: int
    description: Optional[str]


class LineType(str, Enum):
    material = "Material"
    hex = "HEX"
    btp = "BTP"
    hex_additions = "HEXAdditions"
    auto_shield = "AutoShield"
    tdu = "TDU"
    pump = "Pump"
    unknown = "UNKNOWN"

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        use_enum_values=True
    )


class DocumentType(str, Enum):
    Not = "Not"
    ordered_by_distributor = "OrderedByDistributor"
    on_transit_from_distributor = "OnTransitFromDistributor"
    order = "Order"
    part_r = "PartR"

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class Transit(BaseModel):
    quantity: float = Field(description='Количество, зарезервированное в поставке для заказа')
    date: datetime = Field(description='Дата поступления на склад')
    document_type: DocumentType = Field(
        description='Типы документов транзита. Allowed: Not┃OrderedByDistributor┃OnTransitFromDistributor┃Order┃PartR')

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class Availability(BaseModel):
    requested_qty: int = Field(description='Запрошенное количество')
    on_stock_qty: int = Field(description='Наличие товара на складе.')
    transit: Optional[List[Transit]] = Field(
        description='Список ожидаемых поставок для удовлетворения запрошенного количества', default_factory=list)
    on_transit_qty: int = Field(
        description='Количество, ожидаемое к поступлению на склад для удовлетворения запрошенного количества')
    transit_date: Optional[datetime] = Field(
        description='Дата, к которой запрошенное количество полностью поступит на склад.')
    not_available_qty: int = Field(
        description='Количество, недоступное на складе и в транзите. '
                    'NotAvailableQty = RequestedQty - OnStockQty - SUM(Transit)')
    delivery_weeks: int = Field(
        description='Стандартный срок готовности к отгрузке со склада в рабочих днях')
    delivery_days: Optional[int] = Field(description='Стандартный срок готовности к отгрузке со склада в рабочих днях')
    delivery_time_standard: Optional[str] = Field(
        description='Стандартный срок готовности к отгрузке со склада для количества NotAvailableQty')

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class LockCode(BaseModel):
    id: str = Field(description='Идентификатор')
    description: Optional[str] = Field(description='Описание справочника')


class SourcePrice(BaseModel):
    value: float = Field(description='Значение')
    converted_offer_value: float = Field(description='Значение конвертированное в валюту КП, на дату КП')
    currency: Currency = Field(description='Валюта Allowed: RUB┃EUR┃CUCbr┃CU┃USD┃EUR5┃CNY')

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class SpecialPrice(BaseModel):
    value: float = Field(description='Значение')
    converted_offer_value: float = Field(description='Значение конвертированное в валюту КП, на дату КП')
    currency: Currency = Field(description='Валюта Allowed: RUB┃EUR┃CUCbr┃CU┃USD┃EUR5┃CNY')

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class Calc(BaseModel):
    id: str = Field(description='Уникальный идентификатор расчета (по всех системах)')
    number: Optional[str] = Field(description='Номер расчета')
    calc_type: LineType = Field(
        description='Вид позиции Allowed: Material┃HEX┃BTP┃HEXAdditions┃AutoShield┃TDU┃Pump┃UNKNOWN')

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class BomLines(BaseModel):
    schedules: List[Schedules] = Field(
        deprecated=True,
        description='DEPREACTED. Используйте поле Availability⮕ [ Информация о наличии на складе и поставках ]')
    line_number: int = Field(description='Номер позиции')
    has_promo: bool = Field(description='Флаг о том что к кому можно применить промо курс.')
    source_line_number: int = Field(description='Номер позиции из параметров симуляции')
    material_code: Optional[str] = Field(description='Код материала')
    alt_material_code: Optional[str] = Field(description='Код материала замены')
    description: Optional[str] = Field(description='Описание материала')
    description_extended: Optional[str] = Field(description='Расширенное описание материала')
    sales_price: float = Field(description='Цена из каталога за штуку без НДС')
    width: float = Field(deprecated=True)
    weight: float = Field(description='Вес одной штуки')
    ordered_quantity: int = Field(
        description='Количество заказано. Можеть быть изменено, если заказано некорректное количество.')
    available_quantity: int = Field(deprecated=True, description='DEPREACTED. Используйте поле Availability')
    transit_quantity: int = Field(deprecated=True, description='DEPREACTED. Используйте поле Availability')
    confirmed_delivery_date: Optional[datetime] = Field(deprecated=True,
                                                        description='DEPREACTED. Используйте поле Availability')
    delivery_time_standard: Optional[str] = Field(deprecated=True,
                                                  description='DEPREACTED. Используйте поле Availability')
    surcharges_price: float = Field(description='Итого co скидками и наценками без НДС')
    surcharges_percent: float = Field(description='Процент наценки')
    tax: float = Field(description='Размер налога')
    discount: float = Field(description='Размер скидки')
    discount_percent: float = Field(description='Процент скидки')
    client_discount_percent: float = Field(description='Процент скидки клиента.')
    distr_discount_percent: float = Field(
        description='фактическое значенение скидки для дистра. Если считает дистр на договоре, '
                    'то тут договорная скидка. Если считает конечник, тут значение фактическое для дистра '
                    '(с учетом автопрайнга, объема, комплекта и т.д.)')
    distr_contract_discount: float = Field(description='Договорная скидка дистрибьютора.')
    distr_max_discount: float = Field(description='Максимальная скидка дистрибьютора.')
    approved_discount: Optional[float] = Field(description='Процент согласованной скидки (из OneCRM)')
    currency: Currency = Field(description='Валюта')
    cost: float = Field(description='Себестоимость')
    cost_currency: CostCurrency = Field(description='Валюта Allowed: RUB┃EUR┃CUCbr┃CU┃USD┃EUR5┃CNY')
    sales_price_with_tax: float = Field(description='Итого с наценкой и налогом')
    comments: List[Comments] = Field(description='Комментарии к позиции')
    category: Optional[str] = Field(description='Категория материала([DEPRECATED])', deprecated=True)
    statuses: List[Statuses] = Field(description='Специальные статусы для этой позиции')
    line_type: LineType = Field(description='Вид позиции')
    mpg: Optional[str] = Field(description='ГЦМ')
    material_sub_type: Optional[str] = Field(description='Асортимент материала')
    availability: Optional[Availability] = Field(
        description='Доступность товара и сроки поставки по запрошенному количеству для симуляции. '
                    'Считается из свободных остатков и свободных позиций, ожидаемых поставок на склад')
    is_special_price: bool = Field(description='Специальная цена.')
    is_corrected_quantity: bool = Field(description='Скорректированное количество.')
    allow_create_due_delivery_ticket: bool = Field(
        description='Можно создавать тикет запроса предварительных сроков поставки')
    is_zero_prices: bool = Field(description='Признак нулевой цены на материал')
    lock_code: Optional[LockCode] = Field(description='Справочник ключ(Id)-значение(описание)')
    is_manufacture_reserved: bool = Field(deprecated=True)
    equipment_category_id: Optional[str] = Field(description='Id категории материала.')
    equipment_category: Optional[str] = Field(description='Категория материала.')
    package_size: int = Field(description='Количество в упаковке.')
    promo_currency_value: float = Field(description='Промо курс валюты.')
    auto_distr_pos_discount: float = Field(description='Автоматическая скидка дистра попозицонная.')
    auto_client_pos_discount: float = Field(description='Автоматическая скидка клиента попозицонная')
    exclude_position: bool = Field(description='Отменённая позиция')
    source_price: Optional[SourcePrice] = Field(
        description='Значение в определённой валюте. Очень удобно отдавать в API. '
                    'Т.к. обычно возникает много вопросов, в какой валюте то или иное значение. '
                    'Или "А что это за валюта?". В такой реализации такие недопонимания отпадают')
    special_price: Optional[SpecialPrice] = Field(
        description='Значение в определённой валюте. Очень удобно отдавать в API. '
                    'Т.к. обычно возникает много вопросов, в какой валюте то или иное значение. '
                    'Или "А что это за валюта?". В такой реализации такие недопонимания отпадают')
    calc: Optional[Calc] = Field(description='Информация о расчете')

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        use_enum_values=True
    )


class OrderLine(BaseModel):
    schedules: List[Schedules] = Field(
        deprecated=True,
        description='DEPREACTED. Используйте поле Availability⮕ [ Информация о наличии на складе и поставках ]')
    line_number: int = Field(description='Номер позиции')
    has_promo: bool = Field(description='Флаг о том что к кому можно применить промо курс')
    source_line_number: int = Field(description='Номер позиции из параметров симуляции')
    material_code: Optional[str] = Field(description='Код материала')
    alt_material_code: Optional[str] = Field(description='Код материала замены')
    description: Optional[str] = Field(description='Описание материала')
    description_extended: Optional[str] = Field(description='Расширенное описание материала')
    sales_price: float = Field(description='Цена из каталога за штуку без НДС')
    warranty_price: float = Field(description='Цена гарантии.')
    width: float = Field(deprecated=True)
    weight: float = Field(description='Вес одной штуки')
    ordered_quantity: int = Field(
        description='Количество заказано. Можеть быть изменено, если заказано некорректное количество')
    available_quantity: int = Field(deprecated=True, description='DEPREACTED. Используйте поле Availability')
    transit_quantity: int = Field(deprecated=True, description='DEPREACTED. Используйте поле Availability')
    confirmed_delivery_date: Optional[datetime] = Field(deprecated=True,
                                                        description='DEPREACTED. Используйте поле Availability')
    delivery_time_standard: Optional[str] = Field(deprecated=True,
                                                  description='DEPREACTED. Используйте поле Availability')
    surcharges_price: float = Field(description='Итого co скидками и наценками без НДС')
    surcharges_percent: float = Field(description='Процент наценки')
    tax: float = Field(description='Размер налога')
    discount: float = Field(description='Размер скидки')
    discount_percent: float = Field(description='Процент скидки')
    client_discount_percent: float = Field(description='Процент скидки клиента.')
    distr_discount_percent: float = Field(
        description='фактическое значенение скидки для дистра. Если считает дистр на договоре, '
                    'то тут договорная скидка. Если считает конечник, тут значение фактическое для дистра '
                    '(с учетом автопрайнга, объема, комплекта и т.д.)')
    distr_contract_discount: float = Field(description='Договорная скидка дистрибьютора.')
    distr_max_discount: float = Field(description='Максимальная скидка дистрибьютора.')
    approved_discount: Optional[float] = Field(description='Процент согласованной скидки (из OneCRM)')
    currency: Currency = Field(description='Валюта')
    cost: float = Field(description='Себестоимость')
    cost_currency: CostCurrency = Field(description='Валюта Allowed: RUB┃EUR┃CUCbr┃CU┃USD┃EUR5┃CNY')
    sales_price_with_tax: float = Field(description='Итого с наценкой и налогом')
    comments: List[Comments] = Field(description='Комментарии к позиции')
    category: Optional[str] = Field(description='Категория материала([DEPRECATED])', deprecated=True)
    statuses: List[Statuses] = Field(description='Специальные статусы для этой позиции')
    line_type: LineType = Field(description='Вид позиции')
    mpg: Optional[str] = Field(description='ГЦМ')
    material_sub_type: Optional[str] = Field(description='Асортимент материала')
    availability: Optional[Availability] = Field(
        description='Доступность товара и сроки поставки по запрошенному количеству для симуляции. '
                    'Считается из свободных остатков и свободных позиций, ожидаемых поставок на склад')
    is_special_price: bool = Field(description='Специальная цена.')
    is_corrected_quantity: bool = Field(description='Скорректированное количество.')
    allow_create_due_delivery_ticket: bool = Field(
        description='Можно создавать тикет запроса предварительных сроков поставки')
    is_zero_prices: bool = Field(description='Признак нулевой цены на материал')
    lock_code: Optional[LockCode] = Field(description='Справочник ключ(Id)-значение(описание)')
    equipment_category_id: Optional[str] = Field(description='Id категории материала.')
    equipment_category: Optional[str] = Field(description='Категория материала.')
    package_size: int = Field(description='Количество в упаковке.')
    promo_currency_value: float = Field(description='Промо курс валюты.')
    auto_distr_pos_discount: float = Field(description='Автоматическая скидка дистра попозицонная.')
    auto_client_pos_discount: float = Field(description='Автоматическая скидка клиента попозицонная')
    exclude_position: bool = Field(description='Отменённая позиция')
    source_price: Optional[SourcePrice] = Field(
        description='Значение в определённой валюте. Очень удобно отдавать в API. '
                    'Т.к. обычно возникает много вопросов, в какой валюте то или иное значение. '
                    'Или "А что это за валюта?". В такой реализации такие недопонимания отпадают')
    special_price: Optional[SpecialPrice] = Field(
        description='Значение в определённой валюте. Очень удобно отдавать в API. '
                    'Т.к. обычно возникает много вопросов, в какой валюте то или иное значение. '
                    'Или "А что это за валюта?". В такой реализации такие недопонимания отпадают')
    calc: Optional[Calc] = Field(description='Информация о расчете')
    bomLines: Optional[List[BomLines]] = Field(
        description='Список компонентов позиции заказа ⮕ '
                    '[ Составной элемент позиции заказа с информацией по ценам и наличию ]')

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        use_enum_values=True
    )


class ExchangeRateType(str, Enum):
    CBR = "CBR"
    YRU = "YRU"


class OrderParty(BaseModel):
    currency: Currency = Field(description='Валюта')
    customer_group: Optional[str] = Field(description='Группа', deprecated=True)
    delivery_address: Optional[str] = Field(description='Адрес доставки', deprecated=True)
    delivery_mode: Optional[str] = Field(description='Код условий доставки', deprecated=True)
    delivery_plant: Optional[str] = Field(description='Склад, с которого осуществляется доставка', deprecated=True)
    exchange_rate: float = Field(description='Курс обмена валют (рубли за евро)')
    delivery_mode_text: Optional[str] = Field(description='Описание условий доставки', deprecated=True)
    delivery_plant_name: Optional[str] = Field(description='Название склада', deprecated=True)
    currency_date: Optional[datetime] = Field(description='Дата курса')
    exchange_rate_type: ExchangeRateType = Field(description='Тип курса валют Allowed: CBR┃YRU')

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        use_enum_values=True
    )


class ItPtip(BaseModel):
    name: Optional[str] = Field(description='Имя категории оборудования')
    msg_type: int = Field(description='// 0-красное, 1-желтое, 3-зеленое')
    warn: Optional[str] = Field(description='Текст подсказки')

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class Mpg(BaseModel):
    code: Optional[str] = Field(description='ГЦМ')
    discount_group_description: Optional[str] = Field(description='Описание группы цен материалов для U')

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class DiscountTips(BaseModel):
    discount: Optional[float] = Field(description='Скидка фиксированная.')
    additional_codes: List[str] = Field(description='Список кодов, которые нужно добавить для получения большей скидки')
    group_name: Optional[str] = Field(description='Название группы.')
    equipment_category_id: List[str] = Field(description='Категории материала.')
    additional_discount: Optional[float] = Field(description='Скидка добавочная.')
    current_sum: float = Field(description='Текущая сумма по группе.')
    min_border: Optional[float] = Field(description='Минимальная сумма по группе')
    max_border: Optional[float] = Field(description='Максимальная сумма по группе')
    mpg: List[Mpg] = Field(description='⮕ [ Модель ГЦМ. ]')

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class DiscountTip(BaseModel):
    sum: float
    from_: float = Field(alias="from")
    to: Optional[float]

    class Config:
        populate_by_name = True


class CrmVolumeDiscountTips(BaseModel):
    discount: Optional[float] = Field(description='Скидка фиксированная.')
    additional_codes: List[str] = Field(description='Список кодов, которые нужно добавить для получения большей скидки')
    group_name: Optional[str] = Field(description='Название группы.')
    equipment_category_id: List[str] = Field(description='Категории материала.')
    additional_discount: Optional[float] = Field(description='Скидка добавочная.')
    current_sum: float = Field(description='Текущая сумма по группе.')
    min_border: Optional[float] = Field(description='Минимальная сумма по группе')
    max_border: Optional[float] = Field(description='Максимальная сумма по группе')
    mpg: List[Mpg] = Field(description='⮕ [ Модель ГЦМ. ]')

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class VolumeDiscountTip(BaseModel):
    name: Optional[str] = Field(description='Название группы.')
    crm_volume_discount_tips: List[CrmVolumeDiscountTips]

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class KitDiscountTips(BaseModel):
    discount: Optional[float] = Field(description='Скидка фиксированная.')
    additional_codes: List[str] = Field(description='Список кодов, которые нужно добавить для получения большей скидки')
    group_name: Optional[str] = Field(description='Название группы.')
    id: str
    step_discount: float
    material_code: Optional[str]
    max_discount: float
    is_complete: bool = Field(description='Выполнено условие.')
    equipment_category_id: Optional[str] = Field(description='Категория материала.')
    mpg: List[Mpg] = Field(description='Модель ГЦМ.')

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class KitDiscountTip(BaseModel):
    name: Optional[str] = Field(description='Название группы.')
    type: Optional[str] = Field(description='Тип комплекта')
    kit_discount_tips: List[KitDiscountTips] = Field(
        description='Рекомендации для получения больших скидок⮕ [ Скидки за комплект. ]')

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class AuthoPriceResult(BaseModel):
    auto_price_percent_client_result: float = Field(description='Автоматический процент скидки клиента общий итоговый.')
    auto_price_percent_distr_result: float = Field(
        description='Автоматический процент скидки дистрибьютора общий итоговый.')
    auto_price_client_result: float = Field(description='Автоматическая скидка клиента общая итоговая.')
    auto_price_distr_result: float = Field(description='Автоматическая скидка дистрибьютора общая итоговая.')
    final_markup: float = Field(description='Наценка дистрибьютора.')

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class Object(BaseModel):
    order_lines: List[OrderLine]
    order_party: OrderParty
    it_ptips: Optional[List[ItPtip]]
    discount_tips: Optional[List[DiscountTips]]
    discount_tip: Optional[DiscountTip]
    volume_discount_tips: Optional[List[VolumeDiscountTip]]
    kit_discount_tips: Optional[List[KitDiscountTip]]
    autho_price_results: Optional[AuthoPriceResult]

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class Status(str, Enum):
    Ok = "Ok"
    Warning = "Warning"
    Error = "Error"


class OrderSimulateModel(BaseModel):
    objects: List[Object]
    status: Status = Field(description='Статус ответа Allowed: Ok┃Warning┃Error')
    messages: Optional[List] = Field(
        description='Список сообщений или ошибок, возникших в процессе обработки запроса')
