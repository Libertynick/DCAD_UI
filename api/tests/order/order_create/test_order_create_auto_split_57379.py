import allure
import pytest
from collections import Counter

from api_testing_project.services.order.api.api_order_create import ApiOrderCreate
from api_testing_project.services.order.models.order_create_model import OrderCreateModel
from api_testing_project.services.order.payloads.payloads_order_create import \
    PayloadsOrderCreateMultipleTypes
from api_testing_project.utils.order_split_helper import OrderSplitHelper


@pytest.mark.stage
@pytest.mark.dapi
@allure.feature('DAPI')
@allure.story('Order/Create - автоматическая разбивка заказов по типам материалов')
class TestOrderCreateAutoSplit:
    """
    Набор тестов для проверки автоматической разбивки заказов по типам материалов.

    Система автоматически разбивает заказ на несколько (до 4-х) в зависимости от типов материалов:
    - Группа 1: Material (обычные торговые коды)
    - Группа 2: HEXAdditions (ЗИП и изоляция)
    - Группа 3: TDU, AutoShield, BTP (производственные материалы)
    - Группа 4: HEX, Pump (разборные ПТО и насосы)

    Тесты покрывают все возможные комбинации от 1 до 4 заказов с использованием
    попарного тестирования для полного покрытия функциональности.
    """

    def setup_method(self):
        """
        Инициализация API класса перед каждым тестом.

        Создаёт экземпляр ApiOrderCreate для отправки запросов.
        """
        self.order_create_api = ApiOrderCreate()

    @allure.title('Тест автоматической разбивки заказов: {test_id}')
    @pytest.mark.stage
    @pytest.mark.parametrize('request_payload, expected_orders, test_id', [
        (
                PayloadsOrderCreateMultipleTypes.one_order_material_only,
                1,
                '1 заказ - только Material'
        ),
        (
                PayloadsOrderCreateMultipleTypes.one_order_hex_additions_only,
                1,
                '1 заказ - только HEXAdditions'
        ),
        (
                PayloadsOrderCreateMultipleTypes.one_order_tdu_only,
                1,
                '1 заказ - только TDU'
        ),
        (
                PayloadsOrderCreateMultipleTypes.one_order_hex_only,
                1,
                '1 заказ - только HEX'
        ),
        (
                PayloadsOrderCreateMultipleTypes.one_order_pump_only,
                1,
                '1 заказ - только Pump'
        ),
        (
                PayloadsOrderCreateMultipleTypes.one_order_autoshield_only,
                1,
                '1 заказ - только AutoShield'
        ),
        (
                PayloadsOrderCreateMultipleTypes.one_order_btp_only,
                1,
                '1 заказ - только BTP'
        ),

        (
                PayloadsOrderCreateMultipleTypes.two_orders_material_hex_additions,
                2,
                '2 заказа - Material + HEXAdditions'
        ),
        (
                PayloadsOrderCreateMultipleTypes.two_orders_material_tdu,
                2,
                '2 заказа - Material + TDU'
        ),
        (
                PayloadsOrderCreateMultipleTypes.two_orders_material_hex,
                2,
                '2 заказа - Material + HEX'
        ),
        (
                PayloadsOrderCreateMultipleTypes.two_orders_hex_additions_tdu,
                2,
                '2 заказа - HEXAdditions + TDU'
        ),
        (
                PayloadsOrderCreateMultipleTypes.two_orders_hex_additions_hex,
                2,
                '2 заказа - HEXAdditions + HEX'
        ),
        (
                PayloadsOrderCreateMultipleTypes.two_orders_tdu_hex,
                2,
                '2 заказа - TDU + HEX'
        ),
        (
                PayloadsOrderCreateMultipleTypes.two_orders_material_btp,
                2,
                '2 заказа - Material + BTP'
        ),
        (
                PayloadsOrderCreateMultipleTypes.two_orders_hex_additions_autoshield,
                2,
                '2 заказа - HEXAdditions + AutoShield'
        ),
        (
                PayloadsOrderCreateMultipleTypes.two_orders_hex_additions_btp,
                2,
                '2 заказа - HEXAdditions + BTP'
        ),

        (
                PayloadsOrderCreateMultipleTypes.three_orders_material_hex_additions_tdu,
                3,
                '3 заказа - Material + HEXAdditions + TDU'
        ),
        (
                PayloadsOrderCreateMultipleTypes.three_orders_material_hex_additions_hex,
                3,
                '3 заказа - Material + HEXAdditions + HEX'
        ),
        (
                PayloadsOrderCreateMultipleTypes.three_orders_material_tdu_hex,
                3,
                '3 заказа - Material + TDU + HEX'
        ),
        (
                PayloadsOrderCreateMultipleTypes.three_orders_hex_additions_tdu_hex,
                3,
                '3 заказа - HEXAdditions + TDU + HEX'
        ),

        (
                PayloadsOrderCreateMultipleTypes.four_orders_all_groups,
                4,
                '4 заказа - все группы (Material + HEXAdditions + TDU + HEX/Pump)'
        ),
    ])
    def test_order_create_auto_splits_by_line_types(self, request_payload: dict, expected_orders: int, test_id: str):
        """
        Проверяет автоматическую разбивку заказов по типам материалов.

        Тест выполняет следующие шаги:
        1. Анализирует типы материалов в запросе
        2. Вычисляет ожидаемое количество заказов
        3. Отправляет POST запрос на /api/Order/Create
        4. Проверяет что количество созданных заказов соответствует ожидаемому
        5. Проверяет уникальность offerId и offerNumber
        6. Проверяет что все offerNumber имеют общую базу

        :param request_payload: Payload с материалами для отправки в API.
        :param expected_orders: Ожидаемое количество заказов (от 1 до 4).
        :param test_id: Идентификатор теста для отчётности.

        Ожидаемый результат:
            - Статус ответа "Ok"
            - Количество заказов равно ожидаемому
            - Все offerId уникальны
            - Все offerNumber уникальны
            - Все offerNumber имеют общую базу с разными постфиксами
        """

        print('\n' + '=' * 70)
        print(f'ТЕСТ: {test_id}')
        print('=' * 70)
        print('\n>>> Шаг 1: Анализ материалов в запросе')

        line_types = [line['lineType'] for line in request_payload['orderLines']]
        line_types_count = Counter(line_types)

        print('\nМатериалы в запросе:')
        for line_type, count in sorted(line_types_count.items()):
            print(f'  {line_type}: {count} шт')

        calculated_orders = OrderSplitHelper.calculate_expected_orders_count(request_payload['orderLines'])

        print(f'\nАктивных групп: {calculated_orders}')
        print(f'Ожидаем заказов: {expected_orders}')

        assert calculated_orders == expected_orders, \
            f"Вычисленное количество ({calculated_orders}) не совпадает с ожидаемым ({expected_orders})"

        print('\n>>> Шаг 2: Отправка POST запроса на /api/Order/Create')

        response = self.order_create_api.post_order_create(request_payload)

        print('\n>>> Шаг 3: Проверка статуса ответа')

        status = response['status']
        print(f'\nСтатус ответа: {status}')
        assert status == 'Ok', f"Статус ответа не Ok: {status}"
        print('✓ Статус Ok')

        print('\n>>> Шаг 4: Валидация ответа через Pydantic')

        objects = self.order_create_api.get_objects_from_response(OrderCreateModel)
        assert len(objects) > 0, "Нет объектов в ответе"
        print('✓ Объекты получены')

        print('\n>>> Шаг 5: Проверка количества заказов')

        orders = objects[0].orders
        actual_orders_count = len(orders)

        print(f'\nПолучено заказов: {actual_orders_count}')
        print(f'Ожидалось заказов: {expected_orders}')

        assert actual_orders_count == expected_orders, \
            f"Количество заказов не соответствует ожидаемому. " \
            f"Получено: {actual_orders_count}, ожидалось: {expected_orders}"

        print(f'✓ Количество заказов совпадает: {actual_orders_count} = {expected_orders}')

        print('\n>>> Шаг 6: Проверка уникальности offerId')

        offer_ids = [order.offer_id for order in orders]

        assert OrderSplitHelper.validate_offer_ids_unique(offer_ids), \
            f"offerId не уникальны: {offer_ids}"
        print(f'✓ Все offerId уникальны ({len(offer_ids)} шт)')

        print('\n>>> Шаг 7: Проверка уникальности offerNumber')

        offer_numbers = [order.offer_number for order in orders]
        print(f'\nofferNumbers: {", ".join(offer_numbers)}')

        assert OrderSplitHelper.validate_offer_numbers_unique(offer_numbers), \
            f"offerNumber не уникальны: {offer_numbers}"
        print(f'✓ Все offerNumber уникальны')

        print('\n>>> Шаг 8: Проверка общей базы offerNumber')

        assert OrderSplitHelper.validate_offer_numbers_have_same_base(offer_numbers), \
            f"offerNumber не имеют общей базы: {offer_numbers}"

        base_number = OrderSplitHelper.extract_base_offer_number(offer_numbers[0])
        print(f'✓ Все offerNumber имеют общую базу: {base_number}')

        print('\n>>> Шаг 9: Проверка полей заказов на null')

        for order in orders:
            assert order.offer_id is not None, \
                f"offerId не должен быть None для заказа {order.offer_number}"
            assert order.offer_number is not None, \
                "offerNumber не должен быть None"

        print('✓ Все обязательные поля заполнены')

        print('\n' + '=' * 70)
        print('ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО')
        print('=' * 70 + '\n')