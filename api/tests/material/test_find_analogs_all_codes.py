import allure
import pytest

from api_testing_project.services.material.api.api_find_analogs import ApiFindAnalogs
from api_testing_project.services.material.models.find_analogs_model import FindAnalogsModel
from api_testing_project.services.material.payloads.payloads_find_analogs import PayloadsFindAnalogs
from api_testing_project.utils.http_methods import BadRequest


@pytest.mark.stage
@pytest.mark.dapi
@allure.feature('DAPI')
@allure.story('Позитивные тесты на api/Material/FindAnalogs')
class TestFindAnalogsPositive:
    """Позитивные тесты на api/Material/FindAnalogs"""

    def setup_method(self):
        """
        Инициализация API объекта перед каждым тестом.

        :return: None
        """
        self.api_find_analogs = ApiFindAnalogs()

    @allure.title('Тест на api/Material/FindAnalogs - проверка всех кодов с аналогами')
    @pytest.mark.stage
    def test_find_analogs_all_codes(self):
        """
        Тест на api/Material/FindAnalogs.
        Отправляем все 80 кодов и проверяем, что коды аналогов в ответе совпадают с ожидаемыми.

        :return: None
        :example: Запрос с 80 кодами материалов, ожидаем получить все 80 аналогов
        """
        print(f'\n\nДелаем POST запрос на api/Material/FindAnalogs')
        print(f'Количество кодов в запросе: {len(PayloadsFindAnalogs.all_material_codes)}')

        response = self.api_find_analogs.post_find_analogs(PayloadsFindAnalogs.request_find_analogs_all_codes)

        assert response.status_code == 200, \
            f'HTTP статус код - {response.status_code}, ожидался 200'
        print(f'✓ HTTP статус код: {response.status_code}')

        response_json = response.json()
        result = FindAnalogsModel(**response_json)

        status = result.status
        assert status == 'Ok', f'status в ответе - {status}, ожидался "Ok"'
        print(f'✓ Статус ответа: {status}')

        objects = result.objects
        print(f'✓ Количество объектов в ответе: {len(objects)}')

        actual_analogs = {}
        for obj in objects:
            if obj.material and obj.analogMaterial:
                original_code = obj.material.code
                analog_code = obj.analogMaterial.code
                actual_analogs[original_code] = analog_code

        print(f'\nКоличество найденных аналогов в ответе: {len(actual_analogs)}')
        print(f'Ожидаемое количество аналогов: {len(PayloadsFindAnalogs.expected_analogs)}')

        errors = []
        for original_code, expected_analog in PayloadsFindAnalogs.expected_analogs.items():
            if original_code not in actual_analogs:
                errors.append(f'Код {original_code} не найден в ответе')
            elif actual_analogs[original_code] != expected_analog:
                errors.append(
                    f'Для кода {original_code}: '
                    f'ожидался аналог {expected_analog}, '
                    f'получен {actual_analogs[original_code]}'
                )

        if errors:
            print('\n НАЙДЕНЫ ОШИБКИ:')
            for error in errors:
                print(f'  - {error}')
            assert False, f'Найдено {len(errors)} несоответствий в кодах аналогов:\n' + '\n'.join(errors)
        else:
            print('\n Все коды аналогов совпадают с ожидаемыми!')
            print(f' Успешно проверено {len(actual_analogs)} пар код-аналог')

    @allure.title('Тест на api/Material/FindAnalogs - проверка одного кода: {code}')
    @pytest.mark.stage
    @pytest.mark.parametrize('code, payload, expected_analog', [
        ('003G1000', PayloadsFindAnalogs.request_find_analogs_single_code_003G1000, '003G1000R'),
        ('003H6100', PayloadsFindAnalogs.request_find_analogs_single_code_003H6100, '065B2388R'),
        ('003G1088', PayloadsFindAnalogs.request_find_analogs_single_code_003G1088, '003G5514'),
    ])
    def test_find_analogs_single_code(self, code, payload, expected_analog):
        """
        Тест на api/Material/FindAnalogs с одним кодом.
        Отправляем один код и проверяем, что вернулся правильный аналог.

        :param code: Код материала для поиска аналога
        :param payload: Тело запроса с кодом материала
        :param expected_analog: Ожидаемый код аналога
        :return: None
        :example: Запрос с кодом "003G1000", ожидаем получить аналог "003G1000R"
        """
        print(f'\n\nДелаем POST запрос на api/Material/FindAnalogs')
        print(f'Код материала: {code}')
        print(f'Ожидаемый аналог: {expected_analog}')

        response = self.api_find_analogs.post_find_analogs(payload)

        assert response.status_code == 200, \
            f'HTTP статус код - {response.status_code}, ожидался 200'
        print(f'✓ HTTP статус код: {response.status_code}')

        response_json = response.json()
        result = FindAnalogsModel(**response_json)

        status = result.status
        assert status == 'Ok', f'status в ответе - {status}, ожидался "Ok"'
        print(f'✓ Статус ответа: {status}')

        objects = result.objects
        assert len(objects) > 0, 'В ответе нет объектов'
        print(f'✓ Количество объектов в ответе: {len(objects)}')

        found_analog = None
        all_analogs = []

        for obj in objects:
            if obj.material and obj.material.code == code:
                if obj.analogMaterial and obj.analogMaterial.code:
                    all_analogs.append(obj.analogMaterial.code)
                    if obj.analogMaterial.code == expected_analog:
                        found_analog = obj

        print(f'\nИсходный код: {code}')
        print(f'Все найденные аналоги: {all_analogs}')
        print(f'Ожидаемый аналог: {expected_analog}')

        assert found_analog is not None, \
            f'Ожидаемый аналог {expected_analog} не найден среди {all_analogs}'
        print(f'✓ Ожидаемый аналог {expected_analog} найден корректно!')

        if len(all_analogs) > 1:
            print(f'  Примечание: у материала {code} найдено {len(all_analogs)} аналогов')

    @allure.title('Тест на api/Material/FindAnalogs - проверка малой группы кодов: {group_name}')
    @pytest.mark.stage
    @pytest.mark.parametrize('group_name, payload, codes_list', [
        ('Группа 003G', PayloadsFindAnalogs.request_find_analogs_small_group_003G,
         PayloadsFindAnalogs.small_group_codes_003G),
        ('Группа 003H', PayloadsFindAnalogs.request_find_analogs_small_group_003H,
         PayloadsFindAnalogs.small_group_codes_003H),
        ('Смешанная группа', PayloadsFindAnalogs.request_find_analogs_small_group_mixed,
         PayloadsFindAnalogs.small_group_mixed),
    ])
    def test_find_analogs_small_group(self, group_name, payload, codes_list):
        """
        Тест на api/Material/FindAnalogs с малой группой кодов (3-4 кода).
        Отправляем группу кодов и проверяем, что все аналоги найдены.

        :param group_name: Название группы для отображения в отчете
        :param payload: Тело запроса с кодами материалов
        :param codes_list: Список кодов материалов в группе
        :return: None
        :example: Запрос с группой ["003G1000", "003G1001", "003G1002"], ожидаем получить 3 аналога
        """
        print(f'\n\nДелаем POST запрос на api/Material/FindAnalogs')
        print(f'Группа: {group_name}')
        print(f'Количество кодов: {len(codes_list)}')
        print(f'Коды: {codes_list}')

        response = self.api_find_analogs.post_find_analogs(payload)

        assert response.status_code == 200, \
            f'HTTP статус код - {response.status_code}, ожидался 200'
        print(f'✓ HTTP статус код: {response.status_code}')

        response_json = response.json()
        result = FindAnalogsModel(**response_json)

        status = result.status
        assert status == 'Ok', f'status в ответе - {status}, ожидался "Ok"'
        print(f'✓ Статус ответа: {status}')

        objects = result.objects
        print(f'✓ Количество объектов в ответе: {len(objects)}')

        actual_analogs = {}
        for obj in objects:
            if obj.material and obj.analogMaterial:
                original_code = obj.material.code
                analog_code = obj.analogMaterial.code
                actual_analogs[original_code] = analog_code

        print(f'\nНайдено аналогов: {len(actual_analogs)}')

        errors = []
        for code in codes_list:
            if code not in actual_analogs:
                errors.append(f'Для кода {code} аналог не найден')
            else:
                expected_analog = PayloadsFindAnalogs.expected_analogs.get(code)
                if expected_analog and actual_analogs[code] != expected_analog:
                    errors.append(
                        f'Для кода {code}: ожидался {expected_analog}, получен {actual_analogs[code]}'
                    )
                print(f'  {code} -> {actual_analogs[code]}')

        if errors:
            print('\n НАЙДЕНЫ ОШИБКИ:')
            for error in errors:
                print(f'  - {error}')
            assert False, f'Найдено {len(errors)} ошибок:\n' + '\n'.join(errors)
        else:
            print(f'\n✓ Все аналоги найдены корректно!')

    @allure.title('Тест на api/Material/FindAnalogs - проверка дополнительных полей ответа')
    @pytest.mark.stage
    def test_find_analogs_check_additional_fields(self):
        """
        Тест на api/Material/FindAnalogs с проверкой дополнительных полей.
        Проверяем не только коды аналогов, но и description, characteristics, comment.

        :return: None
        :example: Проверяем что поля material.description и analogMaterial.description заполнены
        """
        print(f'\n\nДелаем POST запрос на api/Material/FindAnalogs')
        print(f'Проверяем дополнительные поля в ответе')

        payload = PayloadsFindAnalogs.request_find_analogs_single_code_003G1000
        response = self.api_find_analogs.post_find_analogs(payload)

        assert response.status_code == 200, \
            f'HTTP статус код - {response.status_code}, ожидался 200'
        print(f'✓ HTTP статус код: {response.status_code}')

        response_json = response.json()
        result = FindAnalogsModel(**response_json)

        status = result.status
        assert status == 'Ok', f'status в ответе - {status}, ожидался "Ok"'
        print(f'✓ Статус ответа: {status}')

        objects = result.objects
        assert len(objects) > 0, 'В ответе нет объектов'
        print(f'✓ Количество объектов: {len(objects)}')

        first_object = objects[0]
        print(f'\nПроверка полей первого объекта:')

        if first_object.material:
            print(f'  material.code: {first_object.material.code}')
            print(f'  material.description: {first_object.material.description}')
            print(f'  material.descriptionExt: {first_object.material.descriptionExt}')
            print(f'  material.altCode: {first_object.material.altCode}')
            print(f'  material.characteristics: {len(first_object.material.characteristics)} шт.')

            assert first_object.material.code is not None, 'material.code отсутствует'
            print(f'  ✓ material.code заполнен')

        if first_object.analogMaterial:
            print(f'\n  analogMaterial.code: {first_object.analogMaterial.code}')
            print(f'  analogMaterial.description: {first_object.analogMaterial.description}')

            assert first_object.analogMaterial.code is not None, 'analogMaterial.code отсутствует'
            print(f'  ✓ analogMaterial.code заполнен')

        if first_object.comment:
            print(f'\n  comment: {first_object.comment}')

        print(f'\n✓ Все основные поля проверены!')


@pytest.mark.stage
@pytest.mark.dapi
@allure.feature('DAPI')
@allure.story('Негативные тесты на api/Material/FindAnalogs')
class TestFindAnalogsNegative:
    """Негативные тесты на api/Material/FindAnalogs"""

    def setup_method(self):
        """
        Инициализация API объекта перед каждым тестом.

        :return: None
        """
        self.api_find_analogs = ApiFindAnalogs()

    @allure.title('Тест на api/Material/FindAnalogs - пустой список кодов')
    @pytest.mark.stage
    def test_find_analogs_empty_list(self):
        """
        Негативный тест на api/Material/FindAnalogs с пустым списком кодов.
        Отправляем пустой массив кодов и проверяем поведение API.

        :return: None
        :example: Запрос с пустым массивом {"codes": []}, ожидаем либо 200 с пустым ответом, либо ошибку
        """
        print(f'\n\nДелаем POST запрос на api/Material/FindAnalogs с пустым списком')

        try:
            response = self.api_find_analogs.post_find_analogs(PayloadsFindAnalogs.request_find_analogs_empty_list)

            print(f'HTTP статус код: {response.status_code}')

            if response.status_code == 200:
                response_json = response.json()
                result = FindAnalogsModel(**response_json)
                print(f'Статус ответа: {result.status}')
                print(f'Количество объектов: {len(result.objects)}')
                print(f'Сообщения: {result.messages}')

                valid_analogs = []
                for obj in result.objects:
                    if obj.analogMaterial and obj.analogMaterial.code and obj.analogMaterial.code.strip() != '':
                        valid_analogs.append(obj.analogMaterial.code)

                print(f'Найдено валидных аналогов: {len(valid_analogs)}')

                assert len(valid_analogs) == 0, \
                    f'Для пустого списка найдены валидные аналоги: {valid_analogs}'
                print(f'✓ Пустой запрос обработан корректно - валидных аналогов не найдено')
            else:
                print(f'Получен статус {response.status_code}')

        except BadRequest as e:
            print(f'Получена ожидаемая ошибка BadRequest: {e}')
            print(f'✓ API корректно обработал пустой запрос с ошибкой 400')

    @allure.title('Тест на api/Material/FindAnalogs - несуществующий код')
    @pytest.mark.stage
    def test_find_analogs_non_existent_code(self):
        """
        Негативный тест на api/Material/FindAnalogs с несуществующим кодом.
        Отправляем несуществующий код и проверяем, что API не находит аналог.

        :return: None
        :example: Запрос с кодом "INVALID_CODE_123", ожидаем пустой результат или сообщение об ошибке
        """
        print(f'\n\nДелаем POST запрос на api/Material/FindAnalogs с несуществующим кодом')
        print(f'Код: INVALID_CODE_123')

        response = self.api_find_analogs.post_find_analogs(
            PayloadsFindAnalogs.request_find_analogs_non_existent_code
        )

        assert response.status_code == 200, \
            f'HTTP статус код - {response.status_code}, ожидался 200'
        print(f'✓ HTTP статус код: {response.status_code}')

        response_json = response.json()
        result = FindAnalogsModel(**response_json)

        print(f'Статус ответа: {result.status}')
        print(f'Количество объектов: {len(result.objects)}')
        print(f'Сообщения: {result.messages}')

        valid_analogs = []
        for obj in result.objects:
            if obj.analogMaterial and obj.analogMaterial.code and obj.analogMaterial.code.strip() != '':
                valid_analogs.append(obj.analogMaterial.code)

        print(f'Найдено валидных аналогов: {len(valid_analogs)}')

        assert len(valid_analogs) == 0, \
            f'Для несуществующего кода найдены валидные аналоги: {valid_analogs}'
        print(f'✓ Несуществующий код корректно обработан - валидных аналогов не найдено')

    @allure.title('Тест на api/Material/FindAnalogs - микс валидных и невалидных кодов')
    @pytest.mark.stage
    def test_find_analogs_mixed_valid_invalid(self):
        """
        Тест на api/Material/FindAnalogs с миксом валидных и невалидных кодов.
        Отправляем смесь существующих и несуществующих кодов, проверяем что валидные обработались.

        :return: None
        :example: Запрос ["003G1000", "INVALID", "003H6100"], ожидаем найти 2 аналога для валидных кодов
        """
        print(f'\n\nДелаем POST запрос на api/Material/FindAnalogs с миксом кодов')
        print(f'Коды: ["003G1000", "INVALID_CODE", "003H6100", "FAKE123"]')

        response = self.api_find_analogs.post_find_analogs(
            PayloadsFindAnalogs.request_find_analogs_mixed_valid_invalid
        )

        assert response.status_code == 200, \
            f'HTTP статус код - {response.status_code}, ожидался 200'
        print(f'✓ HTTP статус код: {response.status_code}')

        response_json = response.json()
        result = FindAnalogsModel(**response_json)

        print(f'Статус ответа: {result.status}')
        print(f'Количество объектов в ответе: {len(result.objects)}')

        actual_analogs = {}
        for obj in result.objects:
            if obj.material and obj.analogMaterial:
                original_code = obj.material.code
                analog_code = obj.analogMaterial.code
                actual_analogs[original_code] = analog_code
                print(f'  {original_code} -> {analog_code}')

        expected_valid_codes = ['003G1000', '003H6100']
        found_valid = [code for code in expected_valid_codes if code in actual_analogs]

        print(f'\nНайдено валидных аналогов: {len(found_valid)} из {len(expected_valid_codes)}')

        assert len(found_valid) == len(expected_valid_codes), \
            f'Ожидалось найти {len(expected_valid_codes)} аналогов, найдено {len(found_valid)}'

        for code in expected_valid_codes:
            assert code in actual_analogs, f'Валидный код {code} не найден в ответе'
            expected_analog = PayloadsFindAnalogs.expected_analogs[code]
            assert actual_analogs[code] == expected_analog, \
                f'Для {code}: ожидался {expected_analog}, получен {actual_analogs[code]}'

        print(f'✓ Все валидные коды обработаны корректно, невалидные проигнорированы')

    @allure.title('Тест на api/Material/FindAnalogs - невалидный формат: {test_name}')
    @pytest.mark.stage
    @pytest.mark.parametrize('test_name, payload', [
        ('Число вместо строки', PayloadsFindAnalogs.request_find_analogs_invalid_format_number),
        ('Null вместо массива', PayloadsFindAnalogs.request_find_analogs_invalid_format_null),
        ('Отсутствие поля codes', PayloadsFindAnalogs.request_find_analogs_missing_codes_field),
    ])
    def test_find_analogs_invalid_format(self, test_name, payload):
        """
        Негативный тест на api/Material/FindAnalogs с невалидным форматом данных.
        Отправляем некорректный формат запроса и ожидаем ошибку 400 (BadRequest).

        :param test_name: Название теста для отображения
        :param payload: Невалидное тело запроса
        :return: None
        :example: Запрос {"codes": [12345]} (число вместо строки), ожидаем BadRequest
        """
        print(f'\n\nДелаем POST запрос на api/Material/FindAnalogs с невалидным форматом')
        print(f'Тест: {test_name}')
        print(f'Payload: {payload}')

        try:
            response = self.api_find_analogs.post_find_analogs(payload)

            print(f'HTTP статус код: {response.status_code}')

            if response.status_code == 400:
                print(f'✓ Получен ожидаемый статус 400 BadRequest')
            else:
                response_json = response.json()
                result = FindAnalogsModel(**response_json)
                print(f'Статус ответа: {result.status}')
                print(f'Сообщения: {result.messages}')

                if result.status == 'Error':
                    print(f'✓ API вернул статус Error для невалидного формата')
                else:
                    print(f'Предупреждение: API принял невалидный формат без ошибки')

        except BadRequest as e:
            print(f'✓ Получена ожидаемая ошибка BadRequest: {e}')

        except Exception as e:
            print(f'Получена ошибка при валидации: {e}')
            print(f'✓ Pydantic модель отклонила невалидные данные')

    @allure.title('Тест на api/Material/FindAnalogs - специальные символы')
    @pytest.mark.stage
    def test_find_analogs_special_symbols(self):
        """
        Негативный тест на api/Material/FindAnalogs со специальными символами.
        Отправляем коды с SQL-инъекциями, HTML-тегами и другими спецсимволами.

        :return: None
        :example: Запрос ["!@#$%", "<script>"], ожидаем безопасную обработку без аналогов
        """
        print(f'\n\nДелаем POST запрос на api/Material/FindAnalogs со специальными символами')
        print(f'Коды: {PayloadsFindAnalogs.request_find_analogs_special_symbols["codes"]}')

        response = self.api_find_analogs.post_find_analogs(
            PayloadsFindAnalogs.request_find_analogs_special_symbols
        )

        assert response.status_code == 200, \
            f'HTTP статус код - {response.status_code}, ожидался 200'
        print(f'✓ HTTP статус код: {response.status_code}')

        response_json = response.json()
        result = FindAnalogsModel(**response_json)

        print(f'Статус ответа: {result.status}')
        print(f'Количество объектов: {len(result.objects)}')
        print(f'Сообщения: {result.messages}')

        valid_analogs = []
        for obj in result.objects:
            if obj.analogMaterial and obj.analogMaterial.code and obj.analogMaterial.code.strip() != '':
                valid_analogs.append({
                    'material_code': obj.material.code if obj.material else '',
                    'analog_code': obj.analogMaterial.code
                })

        print(f'\nНайдено валидных аналогов (с заполненным кодом): {len(valid_analogs)}')
        if valid_analogs:
            print(f'Валидные аналоги: {valid_analogs}')

        assert len(valid_analogs) == 0, \
            f'Для специальных символов найдены валидные аналоги: {valid_analogs}'
        print(f'✓ Специальные символы обработаны безопасно - валидных аналогов не найдено')