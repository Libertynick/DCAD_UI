class PayloadsCreateOffer:
    """Отправляемые данные в API CrmCommerce/CreateOffer"""
    false = False
    true = True
    null = None

    # Базовый валидный шаблон.
    base_valid_offer = {
        "source": "CRM",
        "currency": "RUB",
        "exchangeRateType": "CBR",
        "debtorAccount": "RT25-7705238125-HE",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "paymentTerms": "RU00",
        "deliveryOptions": {
            "consigneeId": "00000000-0000-0000-0000-000000000000"
        },
        "orderLines": [
            {
                "materialCode": "003L0144R",
                "quantity": 1,
                "lineNumber": 1,
                "lineType": "Material"
            }
        ],
        "isDraft": true
    }

    # Delivery options для Industrial (HEX) - доставка до ТК
    delivery_options_dzr_prod_industrial = {
        "ConsigneeCode":null,
  "Condition":"RU",
  "DeliveryCost":0,
  "ClientFinalDelivery":null,
  "ConsigneeContacts":null,
  "consigneeAgreementDelivery":{
    "SourceFiasId":"00000000-0000-0000-0000-000000000000",
    "Address":"",
    "PaidDelivery":false,
    "ConditionDescription":"Стандартные договорные условия",
    "INN":"5249173547"
  },
  "CostIncludedInOrder":false,
  "totalDeliveryWeight":1262.56,
  "endPoint":"ToTK",
  "deliveryType":"PickupDZR",
  "consigneeId":"00000000-0000-0000-0000-000000000000",
  "deliverFullSetOnly":false
}

    # Project Object для Industrial с проектным условием
    project_object_industrial = {
        "id": "9abbcb6b-91ac-4d69-bbee-d0d0f583e18d",  # passportId
        "name": "Детский сад на 240 мест в г. Тарко-Сале, мкр.Южный",
        "address": "Ямало-Ненецкий АО, г Тарко-Сале, мкр Южный",
        "number": 1178586,
        "comment": " "
    }

    # Payload для HR радиаторов с проектным условием
    create_offer_hr_radiator = {
        "orderLines": [],  # Будет заполнено из Simulate
        "isEndUserPQ": False,
        "docType": "Quotation",
        "authorNumber": None,
        "currencyDate": None,
        "exchangeRateType": None,
        "projectDiscountConditions": False,
        "debtorAccount": "RT25-7705238125-HE",
        "finalBuyerCDLId": None,
        "clientInn": None,
        "userComment": "",
        "engineerComment": "",
        "currency": "RUB",
        "methodCode": "ZWEB",
        "purchaseDate": None,  # Будет установлена динамически
        "delayedDeliveryDiscountValue": None,
        "personId": "0b9a97d3-821d-4f84-b016-d3ab2b433bb7",
        "offerId": None,
        "passportId": "9abbcb6b-91ac-4d69-bbee-d0d0f583e18d",
        "opportunityId": None,
        "specTypeId": None,
        "specificationId": "ece5153c-fbbd-4b55-816e-e7dd035364ad",
        "salesGroup": "RU1",
        "salesOffice": "RU01",
        "referenceNumber": "",
        "paymentTerms": "RU00",
        "isDraft": True,
        "purchaseType": None,
        "finalBuyerId": "6e9c40d9-59c3-4576-ab38-8b0724fc92fd",
        "availableForDistributor": False,
        "autoAvailableForDistributor": None,
        "payPercentComponentsBTP": None,
        "payPercentBeforePlacingIntoProduction": None,
        "customerId": None,
        "isCLHOffer": False,
        "deliveryOptions": {
            "consigneeCode": None,
            "deliveryCost": 0,
            "totalDeliveryWeight": 0,
            "comment": "",
            "consigneeAgreementDelivery": None,
            "clientFinalDelivery": None,
            "consigneeContacts": None,
            "endPoint": "ToDoor",
            "desiredDeliveryDate": None,  # Будет установлена динамически
            "deliverFullSetOnly": False,
            "costIncludedInOrder": True,
            "consigneeId": "00000000-0000-0000-0000-000000000000",
            "deliveryType": "Pickup"
        },
        "deliveryOptionsHex": None,
        "deliveryOptionsProd": None,
        "deliveryOptionsDZRProd": None,
        "deliveryNotificationSettings": None,
        "projectObject": {
            "id": "9abbcb6b-91ac-4d69-bbee-d0d0f583e18d",
            "name": "Детский сад на 240 мест в г. Тарко-Сале, мкр.Южный",
            "address": "Ямало-Ненецкий АО, г Тарко-Сале, мкр Южный",
            "number": 1178586,
            "comment": " "
        },
        "setContractDiscounts": False,
        "currencySpecialFixation": False,
        "extendValidit": 0,
        "showPriceWithDiscount": False,
        "showDiscount": False,
        "finalMarkup": None,
        "surchargesPayment": None,
        "surchargesConversion": None,
        "recommendedDistributors": [],
        "source": "WebClient",
        "returnKitDisconts": False,
        "distributorContractId": None
    }