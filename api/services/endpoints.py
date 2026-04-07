from config import TestEnvironment


class Endpoints:
    """Сервисы (методы)"""

    """Получает информацию о клиенте - GetCustomer"""
    get_customer = \
        lambda self, debtor_account: f'{TestEnvironment.BASE_URL_DAPI}api/Customer/GetCustomer?debtorAccount={debtor_account}'
    get_customer_by_inn = lambda self, inn: f'{TestEnvironment.BASE_URL_DAPI}api/Customer/GetCustomerByInn?inn={inn}'
    get_customer_by_number = \
        lambda self, debtor_account: f'{TestEnvironment.BASE_URL_DAPI}api/Customer/GetCustomerByNumber?id={debtor_account}'

    """Рассчитать цены и проверить наличие для материалов - Order/Simulate"""
    post_order_simulate = f'{TestEnvironment.BASE_URL_DAPI}api/Order/Simulate'

    """Создание заказа или КП"""
    post_order_create = f"{TestEnvironment.BASE_URL_DAPI}api/Order/Create"

    """/api/Order/UpdateOffer"""
    post_order_update_offer = f"{TestEnvironment.BASE_URL_DAPI}api/Order/UpdateOffer"

    """Currency"""
    get_conventional_units = lambda self, exchange_rate_type: \
        f'{TestEnvironment.BASE_URL_DAPI}api/Currency/GetConventionalUnits?exchangeRateType={exchange_rate_type}'

    """FullCommerceNew"""
    get_full_commerce_new = \
        lambda self, request_id: f'{TestEnvironment.BASE_URL_DAPI}api/CrmCommerce/FullCommerceNew?requestId={request_id}'

    """/api/CrmCommerce/CreateOffer"""
    post_create_offer = f"{TestEnvironment.BASE_URL_DAPI}api/CrmCommerce/CreateOffer"

    """api/Material/UpdateMaterials"""
    post_update_materials = f'{TestEnvironment.BASE_URL_DAPI}api/Material/UpdateMaterials'

    """api/Material/FindAnalogs"""
    post_find_analogs = f'{TestEnvironment.BASE_URL_DAPI}api/Material/FindAnalogs'

    """/api/Order/CreateDocumentRetry"""
    get_order_create_document_retry = f'{TestEnvironment.BASE_URL_DAPI}api/Order/CreateDocumentRetry'

    """/api/CrmRequest/RequestSave"""
    post_crm_request_request_save = f'{TestEnvironment.BASE_URL_DAPI}api/CrmRequest/RequestSave'

    """ /api/Customer/ReservationThresholdUpdate"""
    post_reservation_threshold_update = f'{TestEnvironment.BASE_URL_DAPI}api/Customer/ReservationThresholdUpdate'

    """/api/Customer/GetCalculationReservationThreshold"""
    get_calculation_reservation_threshold = lambda self, contract_number: f'{TestEnvironment.BASE_URL_DAPI}api/Customer/GetCalculationReservationThreshold?contractNumber={contract_number}'

    """/api/Offer/UpdateOrderInOneCrm"""
    post_update_order_in_one_crm = f"{TestEnvironment.BASE_URL_DAPI}api/Offer/UpdateOrderInOneCrm"

    """/api/CrmCommerce/CommerceList"""
    post_commerce_list = f"{TestEnvironment.BASE_URL_DAPI}api/CrmCommerce/CommerceList"

    """api/Material/FindAndFilter"""
    post_find_and_filter = f'{TestEnvironment.BASE_URL_DAPI}api/Material/FindAndFilter'

    """api/Material/GetMaterialDocument"""
    get_material_document = lambda self, material_code, file_name: \
        f'{TestEnvironment.BASE_URL_DAPI}api/Material/GetMaterialDocument?materialCode={material_code}&fileName={file_name}'

    """/api/Material/UpdateMaterialsPriceCost"""
    post_material_update_materials_price_cost = f'{TestEnvironment.BASE_URL_DAPI}api/Material/UpdateMaterialsPriceCost'

    """/api/Balance/GetOrderPaymentCard"""
    get_balance_get_order_payment_card = lambda self, order_number: f'{TestEnvironment.BASE_URL_DAPI}api/Balance/GetOrderPaymentCard?orderNumber={order_number}'

    """/api/Balance/GetBalance"""
    get_balance = lambda self, inn, organization_inn: f'{TestEnvironment.BASE_URL_DAPI}api/Balance/GetBalance?inn={inn}&organizationInn={organization_inn}'

    """/api/Material/UpdateMaterialsAvaliability"""
    post_material_update_materials_avaliability = f"{TestEnvironment.BASE_URL_DAPI}api/Material/UpdateMaterialsAvaliability"

    """/api/Hex/Save"""
    post_hex_save = f"{TestEnvironment.BASE_URL_DAPI}api/Hex/Save"
