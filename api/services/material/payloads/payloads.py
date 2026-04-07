from faker import Faker


class PayloadsUpdateMaterial:
    """Отправляемые данные на /api/Material/UpdateMaterials"""
    faker = Faker()

    random_article = faker.random_number(digits=10, fix_len=True)  # Рандомное значение для поля MaterialNumber

    false = False
    true = True
    null = None

    # print(random_article)
    create_material = [
        {
            "MaterialNumber": f"{random_article}",
            "ShortDescription": "testing_dapi_api_material_update_materials",
            "Description": f"testing_api_material_update_materials_description_{random_article}",
            "isDeleted": false,
            "PriceCategory": "1D",
            "PackSize": "1",
            "EquipmentCategory": "Поквартирные шкафы отопления",
            "MaterialSegment": "352 ТДУ: готовые TDU.3 ",
            "SalesUnit": "ШТ",
            "WeightUnit": "кг",
            "Weight": "20.100",
            "WeightNet": "23.100",
            "WeightGross": "21.177",
            "WareHouseCategory": "OTHER",
            "Abc": "C",
            "DeliveryTimeStandard": 30,
            "codeComments": "test_dapi",
            "lockCode": false
        }
    ]
    print(create_material)

    update_material = [
        {
            "MaterialNumber": f"{random_article}",
            "ShortDescription": "testing_dapi_api_material_update_materials_v2",
            "Description": f"testing_api_material_update_materials_description_{random_article}_v2",
            "isDeleted": false,
            "PriceCategory": "1D",
            "PackSize": "1",
            "EquipmentCategory": "Поквартирные шкафы отопления",
            "MaterialSegment": "352 ТДУ: готовые TDU.3 ",
            "SalesUnit": "ШТ",
            "WeightUnit": "кг",
            "Weight": "30.100",
            "WeightNet": "23.100",
            "WeightGross": "21.177",
            "WareHouseCategory": "OTHER",
            "Abc": "B",
            "DeliveryTimeStandard": 30,
            "codeComments": "test_dapi_v2",
            "lockCode": false
        }
    ]

    delete_material = [
        {
            "MaterialNumber": f"{random_article}",
            "ShortDescription": "testing_dapi_api_material_update_materials_v2",
            "Description": f"testing_api_material_update_materials_description_{random_article}_v2",
            "isDeleted": true,
            "PriceCategory": "1D",
            "PackSize": "1",
            "EquipmentCategory": "Поквартирные шкафы отопления",
            "MaterialSegment": "352 ТДУ: готовые TDU.3 ",
            "SalesUnit": "ШТ",
            "WeightUnit": "кг",
            "Weight": "30.100",
            "WeightNet": "23.100",
            "WeightGross": "21.177",
            "WareHouseCategory": "OTHER",
            "Abc": "B",
            "DeliveryTimeStandard": 30,
            "codeComments": "test_dapi_v2",
            "lockCode": false
        }
    ]

    blocked_material = [
        {
            "MaterialNumber": f"{random_article}",
            "ShortDescription": "testing_dapi_api_material_update_materials_v2",
            "Description": f"testing_api_material_update_materials_description_{random_article}_v2",
            "isDeleted": false,
            "PriceCategory": "1D",
            "PackSize": "1",
            "EquipmentCategory": "Поквартирные шкафы отопления",
            "MaterialSegment": "352 ТДУ: готовые TDU.3 ",
            "SalesUnit": "ШТ",
            "WeightUnit": "кг",
            "Weight": "30.100",
            "WeightNet": "23.100",
            "WeightGross": "21.177",
            "WareHouseCategory": "OTHER",
            "Abc": "B",
            "DeliveryTimeStandard": 30,
            "codeComments": "test_dapi_v2",
            "lockCode": true
        }
    ]

    add_to_cart_code = {
        "debtorAccount": "RT25-7705238125-HE",
        "materials": [
            {
                "materialCode": f"{random_article}",
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
