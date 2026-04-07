import allure
import pytest

from api_testing_project.services.currency.api.api_currency import CurrencyApi
from api_testing_project.services.currency.models.get_conventional_units_models import GetConventionalUnitsModel
from api_testing_project.services.order.api.api_order_simulate import ApiOrderSimulate
from api_testing_project.services.order.models.order_simulate_model import OrderSimulateModel
from api_testing_project.services.order.payloads.payloads_order_simulate import PayloadsOrderSimulate
from api_testing_project.utils.http_methods import BadRequest


# encoding: utf-8

@pytest.mark.stage
@pytest.mark.dapi
@allure.feature('DAPI')
@allure.story('test for api/Material/UpdateMaterials')
class TestOrderSimulateAddedCodesToCart:
    """Набор тестов на Order/Simulate. Добавление кодов в корзину"""
    api_order_simulate = ApiOrderSimulate()

    @allure.title('Позитивный тест на Order/Simulate на материалы (Добавление в корзину)')
    def test_order_simulate_add_to_cart_material(self):
        """Позитивный тест на Order/Simulate на материалы (Добавление в корзину)"""

        expected_values_dict = {
            'sales_price': 1652.55,  # Ожидаемая Цена из каталога за штуку без НДС (прайс)
            'description': 'LV Ду 15 Клапан запорный прямой никелированный',  # Ожидаемое описание товара
            'discount_percent': 48.0,  # Ожидаемая скидка дистра
            'sales_price_with_tax': 26209.443,  # Итого с наценкой и налогом
            'cost': 0.0,  # Ожидаемая себестоимость
            'currency': 'RUB',  # Ожидаемая валюта
            'line_type': 'Material'  # Ожидаемый тип
        }  # Словарь с ожидаемыми значениями

        print(f'\nДелаем POST запрос в корзину (добавление товара) на Order/Simulate. Код - '
              f'{PayloadsOrderSimulate.order_simulate_add_to_cart_material["materials"][0]["materialCode"]}'
              f' Количество - {PayloadsOrderSimulate.order_simulate_add_to_cart_material["materials"][0]["quantity"]}')

        self.api_order_simulate.post_order_simulate(PayloadsOrderSimulate.order_simulate_add_to_cart_material)
        objects = self.api_order_simulate.get_objects_from_response(OrderSimulateModel)
        order_lines = ApiOrderSimulate.get_order_lines_object_dict(objects)

        result_assert = ApiOrderSimulate.checking_values_from_service_response_by_key(expected_values_dict, order_lines)

        assert len(result_assert) == 0, \
            f'Значения данных полей {result_assert} не соответствует ожидаемым в объекте order_lines!'

    @allure.title('Тест на добавление в корзину расчета - моноблок')
    def test_order_simulate_add_to_cart_monoblock(self):
        """Тест на добавление в корзину расчета - моноблок"""
        expected_values_dict = {
            "sales_price": 156035.45,  # Ожидаемая Цена из каталога за штуку без НДС (прайс)
            "weight": 104.58,  # Вес одной штуки
            "description": 'Аппарат теплообменный пластинчатый разборный НН№14',  # Ожидаемое описание товара
            "discount_percent": 55.0,  # Ожидаемая скидка дистра
            "sales_price_with_tax": 1284951.9307,  # Итого с наценкой и налогом
            "currency": 'RUB',  # Ожидаемая валюта
            "line_type": 'HEX',  # Ожидаемый тип
            "mpg": 'YA'  # ГЦМ
        }  # Словарь с ожидаемыми значениями

        print(f'\nДелаем POST запрос в корзину (добавление товара) на Order/Simulate. Код - '
              f'{PayloadsOrderSimulate.order_simulate_add_to_cart_monoblock["materials"][0]["materialCode"]}'
              f' Количество - {PayloadsOrderSimulate.order_simulate_add_to_cart_monoblock["materials"][0]["quantity"]}')

        self.api_order_simulate.post_order_simulate(PayloadsOrderSimulate.order_simulate_add_to_cart_monoblock)
        objects = self.api_order_simulate.get_objects_from_response(OrderSimulateModel)
        order_lines = ApiOrderSimulate.get_order_lines_object_dict(objects)
        result_assert = ApiOrderSimulate.checking_values_from_service_response_by_key(expected_values_dict, order_lines)

        assert len(result_assert) == 0, \
            f'Значения данных полей {result_assert} не соответствует ожидаемым в объекте order_lines!'

    @allure.title('Тест на добавление кода со спец. ценой')
    def test_order_simulate_add_to_cart_special_price(self):
        """Тест на добавление кода со спец. ценой"""
        expected_values_dict = {
            # "sales_price": 19680.86, # Ожидаемая Цена из каталога за штуку без НДС (прайс)
            "weight": 1.24,  # Вес одной штуки
            "description": 'AMZ 112 двухпозиционный зональный кран , Ду 25 напряжение питания 24 В',
            # Ожидаемое описание товара
            "discount_percent": 0,  # Ожидаемая скидка дистра
            # "sales_price_with_tax": 2665182.0612,  # Итого с наценкой и налогом
            "cost": 0.0,  # Ожидаемая себестоимость
            "currency": 'RUB',  # Ожидаемая валюта
            "line_type": 'Material',  # Ожидаемый тип
            "mpg": '3Z',  # ГЦМ
            "material_code": '082G5402',  # Код материала
            "is_special_price": True,
        }  # Словарь с ожидаемыми значениями

        print(f'\nДелаем POST запрос в корзину (добавление товара) на Order/Simulate. Код - '
              f'{PayloadsOrderSimulate.order_simulate_add_to_cart_special_price["materials"][0]["materialCode"]}'
              f' Количество - {PayloadsOrderSimulate.order_simulate_add_to_cart_special_price["materials"][0]["quantity"]}')

        self.api_order_simulate.post_order_simulate(PayloadsOrderSimulate.order_simulate_add_to_cart_special_price)
        objects = self.api_order_simulate.get_objects_from_response(OrderSimulateModel)
        order_lines = ApiOrderSimulate.get_order_lines_object_dict(objects)
        result_assert = ApiOrderSimulate.checking_values_from_service_response_by_key(expected_values_dict, order_lines)

        assert len(result_assert) == 0, \
            f'Значения данных полей {result_assert} не соответствует ожидаемым в объекте order_lines!'

    @allure.title('Тест на добавление кода с прайсом в УЕ')
    def test_order_simulate_add_to_cart_code_with_price_cu(self):
        """Тест на добавление кода с прайсом в УЕ"""
        # Делаем запрос на получение курса рубля в УЕ
        api_currency = CurrencyApi()
        exchange_rate_type = 'YRU'
        api_currency.get_conventional_units(exchange_rate_type)
        objects_currency = api_currency.get_objects_from_response(GetConventionalUnitsModel)
        currency = objects_currency[0]

        #  Прайс кода в базе всегда 1 уе, поэтому цена кода в рублях равна курсу
        price_code = round(currency, 2)
        print(price_code, 'price_code+++++')

        expected_values_dict = {
            "sales_price": price_code,  # Ожидаемая Цена из каталога за штуку без НДС (прайс)
            "material_code": 'ZZZTEST1YE',  # Код материала
            "description": 'test standart code',  # Ожидаемое описание товара
            "weight": 1,  # Вес одной штуки
            "line_type": 'Material',  # Ожидаемый тип
            "mpg": 'TX',  # ГЦМ
            "discount_percent": 0,  # Ожидаемая скидка дистра

        }  # Словарь с ожидаемыми значениями

        print(f'\nДелаем POST запрос в корзину (добавление товара) на Order/Simulate. Код - '
              f'{PayloadsOrderSimulate.order_simulate_add_to_cart_code_with_price_cu["materials"][0]["materialCode"]} '
              f'Количество - '
              f'{PayloadsOrderSimulate.order_simulate_add_to_cart_code_with_price_cu["materials"][0]["quantity"]}')

        self.api_order_simulate.post_order_simulate(PayloadsOrderSimulate.order_simulate_add_to_cart_code_with_price_cu)
        objects = self.api_order_simulate.get_objects_from_response(OrderSimulateModel)
        order_lines = ApiOrderSimulate.get_order_lines_object_dict(objects)

        result_assert = ApiOrderSimulate.checking_values_from_service_response_by_key(expected_values_dict, order_lines)

        assert len(result_assert) == 0, \
            f'Значения данных полей {result_assert} не соответствует ожидаемым в объекте order_lines!'

    @allure.title('Тест на переключение кода в корзине с рубля на доллары')
    def test_for_switching_code_in_basket_from_rubles_to_cu(self):
        """Тест на переключение кода в корзине с рубля на доллары"""
        expected_values_dict_order_lines = {
            'material_code':
                PayloadsOrderSimulate.order_simulate_request_switching_code_in_basket_from_rubles_to_cu.get(
                    'materials')[0].get('materialCode'),  # Код материала
            'description': 'LV Ду 15 Клапан запорный прямой никелированный',  # Ожидаемое описание товара
            'discount_percent': 48.0,  # Ожидаемая скидка дистра
            'currency': 'CU',  # Ожидаемая валюта
            'cost_currency': 'RUB',  # Валюта себестоимости
            'line_type': 'Material',  # Ожидаемый тип
            'mpg': '1D',  # ГЦМ
            'sales_price_with_tax': 9.1163  # Итого с наценкой и налогом
        }  # Словарь с ожидаемыми значениями объекта order_lines

        self.api_order_simulate.post_order_simulate(
            PayloadsOrderSimulate.order_simulate_request_switching_code_in_basket_from_rubles_to_cu)
        objects = self.api_order_simulate.get_objects_from_response(OrderSimulateModel)

        # Проверка значений в полях объекта order_lines
        order_lines = self.api_order_simulate.get_order_lines_object_dict(objects)

        result_assert = self.api_order_simulate.checking_values_from_service_response_by_key(
            expected_values_dict_order_lines, order_lines)

        assert len(result_assert) == 0, \
            f'Значения данных полей {result_assert} не соответствует ожидаемым в объекте order_lines!'

        # Делаем запрос на получение курса рубля в УЕ
        api_currency = CurrencyApi()
        exchange_rate_type = 'YRU'
        api_currency.get_conventional_units(exchange_rate_type)
        objects_currency = api_currency.get_objects_from_response(GetConventionalUnitsModel)
        currency = objects_currency[0]

        # Проверка значений в полях объекта order_party

        expected_values_dict_order_party = {
            'currency': 'CU',  # Валюта
            'exchange_rate': currency,  # Курс обмена валют (рубли за евро)
            'exchange_rate_type': 'YRU',  # Тип курса валют
            'currency_date': None
        }  # Словарь с ожидаемыми значениями объекта order_party

        order_party = self.api_order_simulate.get_order_party_object_dict(objects)

        result_assert = self.api_order_simulate.checking_values_from_service_response_by_key(
            expected_values_dict_order_party, order_party)

        assert len(result_assert) == 0, \
            f'Значения данных полей {result_assert} не соответствует ожидаемым в объекте order_party!'

    @allure.title('Тест на переключение кода в корзине с доллара на рубли')
    def test_for_switching_code_in_basket_from_cu_to_rubles(self):
        """Тест на переключение кода в корзине с доллара на рубли"""
        expected_values_dict_order_lines = {
            'material_code':
                PayloadsOrderSimulate.order_simulate_request_switching_code_in_basket_from_rubles_to_cu.get(
                    'materials')[0].get('materialCode'),  # Код материала
            'description': 'LV Ду 15 Клапан запорный прямой никелированный',  # Ожидаемое описание товара
            'discount_percent': 48.0,  # Ожидаемая скидка дистра
            'currency': 'RUB',  # Ожидаемая валюта
            'cost_currency': 'RUB',  # Валюта себестоимости
            'line_type': 'Material',  # Ожидаемый тип
            'mpg': '1D',  # ГЦМ
            'cost': 0.0,  # Оценочная себестоимость
            'sales_price': 1652.55,  # Цена из каталога за штуку без НДС
            'sales_price_with_tax': 10483.7772,  # Итого с наценкой и налогом
        }  # Словарь с ожидаемыми значениями объекта order_lines

        self.api_order_simulate.post_order_simulate(
            PayloadsOrderSimulate.order_simulate_request_switching_code_in_basket_from_cu_to_rubles)
        objects = self.api_order_simulate.get_objects_from_response(OrderSimulateModel)
        order_lines = ApiOrderSimulate.get_order_lines_object_dict(objects)
        result_assert = ApiOrderSimulate.checking_values_from_service_response_by_key(
            expected_values_dict_order_lines, order_lines)

        assert len(result_assert) == 0, \
            f'Значения данных полей {result_assert} не соответствует ожидаемым в объекте order_lines!'

        # Делаем запрос на получение курса рубля в УЕ

        exchange_rate_type = 'YRU'
        api_currency = CurrencyApi()
        api_currency.get_conventional_units(exchange_rate_type)
        objects_currency = api_currency.get_objects_from_response(GetConventionalUnitsModel)
        currency = objects_currency[0]

        # Проверка значений в полях объекта order_party

        expected_values_dict_order_party = {
            'currency': 'RUB',  # Валюта
            'exchange_rate': currency,  # Курс обмена валют (рубли за евро)
            'exchange_rate_type': 'YRU',  # Тип курса валют
        }  # Словарь с ожидаемыми значениями объекта order_party

        order_party = self.api_order_simulate.get_order_party_object_dict(objects)

        print(order_party)

        result_assert = self.api_order_simulate.checking_values_from_service_response_by_key(
            expected_values_dict_order_party, order_party)

        assert len(result_assert) == 0, \
            f'Значения данных полей {result_assert} не соответствует ожидаемым в объекте order_party!'

    @allure.title('Тест на добавление в корзину заблокированного кода или несуществующего')
    @pytest.mark.parametrize('payload, expected_description', [
        (PayloadsOrderSimulate.order_simulate_request_add_blocked_code_to_cart, 'Материал заблокирован для сбыта'),
        (PayloadsOrderSimulate.order_simulate_request_add_non_existent_code_to_cart, 'Материал не найден'),
        (PayloadsOrderSimulate.order_simulate_bad_request_add_to_cart_symbols, 'Материал не найден'),
    ])
    def test_for_adding_to_cart_blocked_code_ora_non_existent_code(self, payload, expected_description):
        """Тест на добавление в корзину заблокированного кода или несуществующего"""
        # expected_description = 'Материал заблокирован для сбыта'

        self.api_order_simulate.post_order_simulate(payload)
        objects = self.api_order_simulate.get_objects_from_response(OrderSimulateModel)

        order_lines = objects[0].order_lines
        statuses = order_lines[0].statuses
        description = statuses[0].description

        assert description == expected_description, \
            f'Ожидаемое описание в заблокированном товаре (поле description) - ({expected_description}) не ' \
            f'соответствует описанию в ответе - ({description})'

    @allure.title('Тест на добавление в корзину некорректного кода (bad request)')
    @pytest.mark.parametrize('material_code, expected_messages', [
        pytest.param(
            '  ', 'Запрос должен содержать хотя бы один код материала',
            id='"  ", Запрос должен содержать хотя бы один код материала'
        ),
        pytest.param(
            'privet', [], id=f'privet, {[]}'
        ),
        pytest.param(
            None, 'Запрос должен содержать хотя бы один код материала',
            id=f'{None}, Запрос должен содержать хотя бы один код материала'
        )

    ])
    def test_with_adding_incorrect_code(self, material_code, expected_messages):
        """Тест на добавление в корзину некорректного кода (bad request)"""
        try:
            payload = PayloadsOrderSimulate.order_simulate_bad_request_add_to_cart_symbols
            payload = payload['materials'][0]['materialCode']
            response = self.api_order_simulate.post_order_simulate(payload)
            return response
        except BadRequest as e:
            print()
            print('Ожидаемая ошибка-', e)
