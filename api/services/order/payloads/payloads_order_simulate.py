class PayloadsOrderSimulate:
    """Отправляемые данные в API Order/Simulate"""
    false = False
    true = True
    null = None

    #  Запрос на добавление в корзину материалов (стандартный запрос, без спец. условий)
    order_simulate_add_to_cart_material = {
        "debtorAccount": "RT25-7705238125-HE",
        "materials": [
            {
                "materialCode": "003L0144R",
                "quantity": 25,
                "lineNumber": 1,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    # Запрос на добавление в корзину ПТО (стандартный запрос, без спец. условий)
    order_simulate_add_to_cart_pto = {
        "debtorAccount": "RT25-7705238125-HE",
        "materials": [
            {
                "materialCode": "878139",
                "quantity": 10,
                "lineNumber": 1,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    #  Запрос на добавление в корзину расчета - моноблок (стандартный запрос, без спец. условий)
    order_simulate_add_to_cart_monoblock = {
        "debtorAccount": "RT25-7705238125-HE",
        "materials": [
            {
                "materialCode": "w102207033",
                "quantity": 15,
                "lineNumber": 0,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    #  Запрос на добавление в корзину насоса (стандартный запрос, без спец. условий)
    order_simulate_add_to_cart_pumps = {
        "debtorAccount": "RT25-7705238125-HE",
        "materials": [
            {
                "materialCode": "Q1512230012-1",
                "quantity": 25,
                "lineNumber": 0,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    #  Запрос на добавление в корзину БОМов (стандартный запрос, без спец. условий)
    order_simulate_add_to_cart_bom = {
        "debtorAccount": "RT25-7705238125-HE",
        "materials": [
            {
                "materialCode": "065B2979R",
                "quantity": 7,
                "lineNumber": 0,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    #  Запрос на добавление в корзину ША БАСТ (стандартный запрос, без спец. условий)
    order_simulate_add_to_cart_bast = {
        "debtorAccount": "RT25-7705238125-HE",
        "materials": [
            {
                "materialCode": "BAST3011254401",
                "quantity": 11,
                "lineNumber": 0,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    #  Запрос на добавление в корзину ЗИП (стандартный запрос, без спец. условий)
    order_simulate_add_to_cart_zip = {
        "debtorAccount": "RT25-7705238125-HE",
        "materials": [
            {
                "materialCode": "089U1029",
                "quantity": 101,
                "lineNumber": 0,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    #  Запрос на добавление в корзину TDU (стандартный запрос, без спец. условий)
    order_simulate_add_to_cart_tdu = {
        "debtorAccount": "RT25-7705238125-HE",
        "materials": [
            {
                "materialCode": "TDU1009575",
                "quantity": 10,
                "lineNumber": 0,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    # Запрос на добавление в корзину кода со спец. ценой
    order_simulate_add_to_cart_special_price = {
        "debtorAccount": "RT25-7705238125-HE",
        "materials": [
            {
                "materialCode": "082G5402",
                "quantity": 111,
                "lineNumber": 1,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    # Запрос на добавление в корзину кода с прайсом в уе
    order_simulate_add_to_cart_code_with_price_cu = {
        "debtorAccount": "RT25-7705238125-HE",
        "materials": [
            {
                "materialCode": "ZZZTEST1YE",
                "quantity": 1,
                "lineNumber": 1,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": "YRU",
        "returnAutoPrice": false
    }

    # Запрос на переключение кода в корзине с рублей на уе
    order_simulate_request_switching_code_in_basket_from_rubles_to_cu = {
        "debtorAccount": "RT25-7705238125-HE",
        "materials": [
            {
                "materialCode": "003L0144R",
                "quantity": 1,
                "lineNumber": 0,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "CU",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    # Запрос на переключение кода в корзине с уе на рубли
    order_simulate_request_switching_code_in_basket_from_cu_to_rubles = {
        "debtorAccount": "RT25-7705238125-HE",
        "materials": [
            {
                "materialCode": "003L0144R",
                "quantity": 10,
                "lineNumber": 0,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    # Запрос на добавление в корзину заблокированного кода
    order_simulate_request_add_blocked_code_to_cart = {
        "debtorAccount": "RT25-7705238125-HE",
        "materials": [
            {
                "materialCode": "004B1201",
                "quantity": 99,
                "lineNumber": 1,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    # Запрос на добавление в корзину несуществующего кода
    order_simulate_request_add_non_existent_code_to_cart = {
        "debtorAccount": "RT25-7705238125-HE",
        "materials": [
            {
                "materialCode": "87813",
                "quantity": 1,
                "lineNumber": 0,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    # Запрос на добавление в корзину символов
    order_simulate_bad_request_add_to_cart_symbols = {
        "debtorAccount": "RT25-7705238125-HE",
        "materials": [
            {
                "materialCode": "!@#$%%",
                "quantity": 1,
                "lineNumber": 0,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    # Запрос на добавление в корзину BTP (стандартный запрос, без спец. условий)
    order_simulate_add_to_cart_btp = {
        "debtorAccount": "RT25-7705238125-HE",
        "materials": [
            {
                "materialCode": "N2811259199-1",
                "quantity": 2,
                "lineNumber": 0,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    # Запрос на добавление в корзину Industrial (HEX - теплообменник) с проектным условием
    order_simulate_add_to_cart_industrial = {
        "debtorAccount": "31/25-CH",
        "materials": [
            {
                "materialCode": "w202102975",
                "quantity": 1,
                "lineNumber": 1,
                "usePromoCurrency": False,
                "useSpecialPrice": True,
                "odid": None
            }
        ],
        "paymentTerms": "RU00",
        "personId": "b898f86a-6070-451b-9a14-47ba949c8cb8",
        "offerId": None,
        "returnEndClientDiscount": False,
        "currency": "RUB",
        #"currencyDate": "2025-10-15T00:00:00",
        "exchangeRateType": "YRU",
        "returnAutoPrice": False,
        "surchargesPayment": "0",
        "surchargesConversion": 0,
        "returnKitDisconts": True,
        "returnVolumeDisconts": True,
        "returnAdditionalBTP": False,
        "extendedWarranty": {"type": "0"},
        "isEstimateOffer": False
    }

    # Запрос на добавление в корзину радиатора HR
    order_simulate_add_to_cart_radiator = {
        "debtorAccount": "RT25-7705238125-HE",
        "materials": [
            {
                "materialCode": "HR00045",
                "quantity": 2,
                "lineNumber": 0,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    # Запрос на добавление в корзину теплообменника Клевер Хит (HEX с промовалютой)
    order_simulate_add_to_cart_clover_hit = {
        "debtorAccount": "RT25-7705238125-HE",
        "materials": [
            {
                "materialCode": "w003013006",
                "quantity": 1,
                "lineNumber": 1,
                "usePromoCurrency": true,
                "useSpecialPrice": true,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "f8eaae4a-1309-4b24-95e8-3a092dc30067",
        "offerId": null,
        "currency": "RUB",
        "currencyDate": "2025-11-05T00:00:00",
        "exchangeRateType": "YRU",
        "returnAutoPrice": false,
        "surchargesPayment": "0",
        "surchargesConversion": 0,
        "specificationId": "0e59258b-b7aa-434f-877e-efd37be5930f",
        "returnKitDisconts": true,
        "returnVolumeDisconts": true,
        "returnAdditionalBTP": false,
        "extendedWarranty": {"type": "0"},
        "isEstimateOffer": false
    }