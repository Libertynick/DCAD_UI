from datetime import datetime, timedelta
from typing import Dict, Optional


class PayloadsUpdateOrderInOneCrm:
    """
    Класс с payload'ами для метода /api/Offer/UpdateOrderInOneCrm

    Содержит базовые данные заказа и методы для создания различных вариантов
    payload'ов для позитивных и негативных тестов.

    Позитивные тесты: 3 метода для обновления различных полей
    Негативные тесты: 3 метода для проверки отсутствия обязательных полей

    Используется для тестирования обновления существующих заказов в системе OneCRM.
    """

    false = False
    true = True
    null = None

    @staticmethod
    def get_base_payload() -> Dict:
        """
        Базовый payload для обновления заказа RT25-070765

        Возвращает полный payload со всеми необходимыми полями для успешного обновления заказа.
        Этот payload используется как основа для всех тестовых сценариев.

        :return: Полный словарь с данными заказа

        Основные поля:
            - DocumentNumber: Номер документа заказа
            - QuotationNumber: Номер коммерческого предложения (PQ04813171-1)
            - Materials: Список материалов в заказе
            - StagesSchedulePayment: Этапы оплаты
            - Organization: Данные организации-контрагента
        """
        return {
            "Completed": "1",
            "Deleted": "0",
            "Date": "30.12.2025 11:51:16",
            "DocumentNumber": "RT26-012080",
            "QuotationNumber": "PQ04848851-1",
            "HeadOffice": "ФИРМА ВОДОКОМФОРТ (7705238125)",
            "PartnerSAPID": "",
            "PartnerINN": "7705238125",
            "PartnerNamе": "ФИРМА ВОДОКОМФОРТ (7705238125)",
            "Organization_old": "ООО \"Ридан Трейд\"",
            "Currency": "руб.",
            "TotalAmount": 1640.54,
            "Warehouse": "0010 Склад Лешково ",
            "ContractNumber": "RT25-7705238125-HE",
            "PaymentTermsCode": "RU00",
            "TaxIncluded": "0",
            "ResponsibleEngineer": "Семенов Даниил Александрович",
            "AddlInfo": "test_order_create",
            "CompleteDelivery": False,
            "Status": "К выполнению / В резерве",
            "CurrentStatus": "Ожидается оплата до обеспечения",
            "PaymentPercent": 0,
            "PrepayAmountToCollect": 1640.54,
            "PrepayAmountToDelivery": 0,
            "DeliveryDate": "",
            "DaliveryDate": "",
            "DeliveryAddress": "Нет данных",
            "TaxType": "Продажа облагается НДС",
            "DelayedDeliveryDiscountValue": 0,
            "DeliveryCost": 0,
            "DiscountsCalculated": "1",
            "EngineerComment": "Заказ создан 2025-12-30T11:51:16.124251+03:00 Тест НЕ_РАЗМЕЩАТЬ_НИЧЕГО (k.tertyshnyi@vodokomfort.ru)  +7 (906) 034-13-83\ntest_order_create",
            "ClientCommen": "test_order_create",
            "ReferenceNumber": "Z0000052452",
            "ReferenceDate": "30.12.2025",
            "ConsigneeSAPID": "",
            "Consignee": "",
            "ConsigneeName": "",
            "SalesDepartmentName": "4101 Отдел продаж тепловой автоматики Москва",
            "SalesDepartmentCode": "4101",
            "Author": "http_robot",
            "DeliveryType": "Силами перевозчика",
            "DeliveryPartner": "Самовывоз",
            "DeliveryAddressValue": "",
            "DeliveryAddlInfo": "Доставка до двери.",
            "ContactPerson": "Арсланов ",
            "SalesGroup": "",
            "PaidInCurrency": "0",
            "Organization": {
                "ContractorId": "00000000-0000-0000-0000-000000000000",
                "INN": "5017132318",
                "ContractorName": "ООО \"Ридан Трейд\""
            },
            "Materials": [
                {
                    "LineNo": 1,
                    "DeliveryDate": "",
                    "ODID": "730cafa2-7c5c-4fb1-a0d7-6c07e807016d",
                    "MaterialNumber": "003L0144R",
                    "MaterialName": "LV Ду 15 Клапан запорный прям. никелир.",
                    "PackType": "шт",
                    "PacksAmount": 2,
                    "AmountInWareUnits": 2,
                    "PriceCondition": "",
                    "Price": 683.56,
                    "Amount": 1367.12,
                    "Tax": "20%",
                    "TaxAmount": 273.42,
                    "AmountWithTax": 1640.54,
                    "DiscountPercent": 0,
                    "DiscountAmount": 0,
                    "AutoDiscountPercent": 0,
                    "AutoDiscountAmount": 0,
                    "CancelReason": "",
                    "Code": 1,
                    "Cancelled": "0",
                    "RelationshipKey": 0,
                    "Warehouse": "0010 Склад Лешково ",
                    "DeliveryDays": 0,
                    "Description": "",
                    "SupplyType": "Не обеспечивать",
                    "CollectionTypeNumber": "",
                    "CollectionTypeName": "",
                    "SalesDepartmentName": "",
                    "SalesDepartmentCode": "",
                    "Stock": 7161,
                    "Reservation": 1816,
                    "OnStock": 8977,
                    "Transit": [
                        {
                            "Quantity": 2,
                            "Date": None,
                            "Status": "Не обеспечивать",
                            "TransitComment": ""
                        }
                    ]
                }
            ],
            "StagesSchedulePayment": [
                {
                    "LineNo": 1,
                    "PaymentType": "Оплата до обеспечения",
                    "Date": (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y"),
                    "PaymentPercent": 100,
                    "Amount": 1640.54,
                    "PaymentMove": 1,
                    "PaymentMoveType": "от даты заказа"
                }
            ],
            "CompleteDeliveryFrom": None,
            "PaidStorage": []
        }

    @staticmethod
    def update_dates_and_comments(base_payload: Dict, update_dates: bool = True,
                                  update_comments: bool = True,
                                  custom_comment: Optional[str] = None,
                                  custom_addl_info: Optional[str] = None) -> Dict:
        """
        Обновляет даты и комментарии в базовом payload

        Метод создает копию базового payload и обновляет в нем:
        - Дату документа (Date)
        - Дату референса (ReferenceDate)
        - Дату оплаты (StagesSchedulePayment[0].Date)
        - Комментарий клиента (ClientCommen)
        - Дополнительную информацию (AddlInfo)

        :param base_payload: Базовый payload для обновления
        :param update_dates: Если True - обновляет все даты на текущие
        :param update_comments: Если True - обновляет комментарии
        :param custom_comment: Пользовательский комментарий клиента (если не указан - генерируется автоматически)
        :param custom_addl_info: Пользовательская дополнительная информация (если не указана - генерируется автоматически)
        :return: Обновленный payload с новыми датами и комментариями

        Example:
            base = PayloadsUpdateOrderInOneCrm.get_base_payload()
            updated = PayloadsUpdateOrderInOneCrm.update_dates_and_comments(base)
            print(updated["ClientCommen"])
            # test_order_create - ОБНОВЛЕНО 2025-01-26 12:30:45
        """
        payload = dict(base_payload)

        if update_dates:
            new_date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            new_ref_date = datetime.now().strftime("%d.%m.%Y")
            new_payment_date = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")

            payload["Date"] = new_date
            payload["ReferenceDate"] = new_ref_date
            payload["StagesSchedulePayment"][0]["Date"] = new_payment_date

        if update_comments:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            payload["ClientCommen"] = custom_comment if custom_comment else f"test_order_create - ОБНОВЛЕНО {timestamp}"
            payload["AddlInfo"] = custom_addl_info if custom_addl_info else f"Тест обновления заказа - {timestamp}"

        return payload

    @staticmethod
    def update_delivery_info(base_payload: Dict, delivery_date: Optional[str] = None,
                             delivery_address: Optional[str] = None,
                             delivery_partner: Optional[str] = None,
                             contact_person: Optional[str] = None) -> Dict:
        """
        Обновляет информацию о доставке в базовом payload

        Метод позволяет изменить данные, связанные с доставкой заказа:
        - Дату доставки
        - Адрес доставки
        - Партнера по доставке
        - Контактное лицо

        :param base_payload: Базовый payload для обновления
        :param delivery_date: Новая дата доставки (формат: "DD.MM.YYYY" или "DD.MM.YYYY HH:MM:SS")
        :param delivery_address: Новый адрес доставки
        :param delivery_partner: Новый партнер по доставке (например: "Самовывоз", "СДЭК")
        :param contact_person: Новое контактное лицо для доставки
        :return: Обновленный payload с новыми данными доставки

        Example:
            base = PayloadsUpdateOrderInOneCrm.get_base_payload()
            updated = PayloadsUpdateOrderInOneCrm.update_delivery_info(
                base,
                delivery_address="г. Москва, ул. Ленина, д. 1",
                contact_person="Иванов Иван"
            )
        """
        payload = dict(base_payload)

        if delivery_date:
            payload["DeliveryDate"] = delivery_date
        if delivery_address:
            payload["DeliveryAddress"] = delivery_address
        if delivery_partner:
            payload["DeliveryPartner"] = delivery_partner
        if contact_person:
            payload["ContactPerson"] = contact_person

        return payload

    @staticmethod
    def update_financial_fields(base_payload: Dict, prepay_amount: Optional[float] = None,
                                delivery_cost: Optional[float] = None,
                                discount_value: Optional[float] = None) -> Dict:
        """
        Обновляет финансовые поля в базовом payload

        Метод изменяет финансовые параметры заказа:
        - Сумму предоплаты к получению
        - Стоимость доставки
        - Скидку за отложенную доставку

        :param base_payload: Базовый payload для обновления
        :param prepay_amount: Новая сумма предоплаты к получению (в рублях)
        :param delivery_cost: Новая стоимость доставки (в рублях)
        :param discount_value: Новое значение скидки за отложенную доставку (в рублях)
        :return: Обновленный payload с новыми финансовыми данными

        Example:
            base = PayloadsUpdateOrderInOneCrm.get_base_payload_rt25_070765()
            updated = PayloadsUpdateOrderInOneCrm.update_financial_fields(
                base,
                prepay_amount=2000.00,
                delivery_cost=500.00
            )
        """
        payload = dict(base_payload)

        if prepay_amount is not None:
            payload["PrepayAmountToCollect"] = prepay_amount
        if delivery_cost is not None:
            payload["DeliveryCost"] = delivery_cost
        if discount_value is not None:
            payload["DelayedDeliveryDiscountValue"] = discount_value

        return payload

    @staticmethod
    def negative_missing_document_number() -> Dict:
        """
        НЕГАТИВНЫЙ ТЕСТ: Отсутствует обязательное поле DocumentNumber

        Удаляет из payload обязательное поле "DocumentNumber" (номер заказа).
        Ожидаемый результат: API должен вернуть ошибку, т.к. без номера заказа
        невозможно идентифицировать какой заказ нужно обновить.

        :return: Payload без поля DocumentNumber

        Ожидаемый статус ответа: "Error"
        Ожидаемое сообщение: Ошибка валидации о том, что DocumentNumber обязателен
        """
        payload = PayloadsUpdateOrderInOneCrm.get_base_payload()
        del payload["DocumentNumber"]
        return payload

    @staticmethod
    def negative_missing_quotation_number() -> Dict:
        """
        НЕГАТИВНЫЙ ТЕСТ: Отсутствует обязательное поле QuotationNumber

        Удаляет из payload обязательное поле "QuotationNumber" (номер КП).
        Ожидаемый результат: API должен вернуть ошибку, т.к. заказ должен быть
        привязан к коммерческому предложению.

        :return: Payload без поля QuotationNumber

        Ожидаемый статус ответа: "Error"
        Ожидаемое сообщение: Ошибка валидации о том, что QuotationNumber обязателен
        """
        payload = PayloadsUpdateOrderInOneCrm.get_base_payload()
        del payload["QuotationNumber"]
        return payload

    @staticmethod
    def negative_missing_organization() -> Dict:
        """
        НЕГАТИВНЫЙ ТЕСТ: Отсутствует объект Organization

        Удаляет из payload обязательный объект "Organization" с данными контрагента.
        Ожидаемый результат: API должен вернуть ошибку, т.к. для заказа
        необходимо указать организацию-контрагента.

        :return: Payload без объекта Organization

        Ожидаемый статус ответа: "Error"
        Ожидаемое сообщение: Ошибка валидации об отсутствии Organization
        """
        payload = PayloadsUpdateOrderInOneCrm.get_base_payload()
        del payload["Organization"]
        return payload