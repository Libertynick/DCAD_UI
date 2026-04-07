class PayloadsOrderUpdateOffer:
    """Отправляемые данные в API Order/UpdateOffer"""
    false = False
    true = True
    null = None

    # Минимальный payload для UpdateOffer - только обязательные поля
    base_update_offer = {
        "source": "CRM",
        "currency": "RUB",
        "exchangeRateType": "CBR",
        "debtorAccount": "RT25-7705238125-HE",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "paymentTerms": "RU00",
        "offerId": null,
        "opportunityId": null,
        "orderLines": [],
        "deliveryOptions": {
            "consigneeId": "00000000-0000-0000-0000-000000000000"
        },
        "isDraft": false  # ← ДОБАВИТЬ ЭТУ СТРОКУ!
    }