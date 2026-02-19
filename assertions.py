import json
from typing import Any, Optional

import allure


def assert_eq(
        actual_value: Any,
        expected_value: Any,
        allure_title: str,
        error_message: Optional[str] = None
) -> None:
    """
    Строгое сравнение значений на равенство
    :param actual_value: Актуальное значение для сравнения
    :param expected_value: Ожидаемое значение
    :param allure_title: Описание шага для allure отчета
    :param error_message: Сообщение об ошибке в случае неравенства значений
    """
    with allure.step(allure_title):
        try:
            assert actual_value == expected_value, error_message or 'Сравниваемые значения не равны'

        except AssertionError:
            attach_data = {
                'actual_value': actual_value,
                'expected_value': expected_value
            }
            _allure_attach_error(attach_response=attach_data, error_name='Ошибка сравнения значений')
            raise


def assert_not_eq(
        actual_value: Any,
        value_not_eq: Any,
        allure_title: str,
        error_message: Optional[str] = None
) -> None:
    """
    Строгое сравнение значений на неравенство
    :param actual_value: Актуальное значение для сравнения
    :param value_not_eq: Значение, которому не равно
    :param allure_title: Описание шага для allure отчета
    :param error_message: Сообщение об ошибке в случае равенства значений
    """
    with allure.step(allure_title):
        try:
            assert actual_value != value_not_eq, error_message or 'Сравниваемые значения равны'

        except AssertionError:
            attach_data = {
                'actual_value': actual_value,
                'expected_value': value_not_eq
            }
            _allure_attach_error(attach_response=attach_data, error_name='Ошибка сравнения значений')
            raise


def assert_eq_with_acceptable_error(
        actual_value: Any,
        expected_value: Any,
        permissible_error: Any,
        allure_title: str,
        error_message: Optional[str] = None
):
    """
    Проверка на равенство с допустимой погрешностью
    :param actual_value: Актуальное значение для сравнения
    :param expected_value: Значение, которому равно
    :param permissible_error: Значение допустимой погрешности при сравнении
    :param allure_title: Описание шага для allure отчета
    :param error_message: Сообщение об ошибке в случае равенства значений
    """
    with allure.step(allure_title):
        try:
            assert abs(actual_value - expected_value) < permissible_error, error_message or (
                f'Сравниваемые значения не равны. '
                f'Погрешность при сравнении - {permissible_error}')

        except AssertionError:
            attach_data = {
                'actual_value': actual_value,
                'expected_value': expected_value,
                'Допустимая погрешность': permissible_error
            }
            _allure_attach_error(attach_response=attach_data, error_name='Ошибка сравнения значений')
            raise


def assert_contains(
        actual_value: Any,
        expected_contains: Any,
        allure_title: str,
        error_message: Optional[str] = None
) -> None:
    """
    Проверка содержания значения в элементе
    :param actual_value: Актуальное значение
    :param expected_contains: Ожидаемое значение, которое содержится в элементе
    :param allure_title: Описание шага для allure отчета
    :param error_message: Сообщение об ошибке в случае неравенства значений
    """
    with allure.step(allure_title):
        try:
            assert expected_contains in actual_value, error_message or f'Значение {expected_contains} не содержится в {actual_value}'

        except AssertionError:
            attach_data = {
                'actual_value': actual_value,
                'expected_value': expected_contains
            }
            _allure_attach_error(attach_response=attach_data,
                                 error_name='Ошибка при проверки содержания значения в элементе')
            raise


def assert_greater_than(
        greater_value: Any,
        less_value: Any,
        allure_title: str,
        error_message: Optional[str] = None
):
    """Проверка, что одно значение больше другого
    :param greater_value: Значение, которое должно быть больше
    :param less_value: Значение, которое меньше
    :param allure_title: Описание шага для allure отчета
    :param error_message: Сообщение об ошибке в случае равенства значений
    """

    with allure.step(allure_title):
        try:
            assert greater_value > less_value, error_message or f'Значение {greater_value} меньше или равно {less_value}'

        except AssertionError:
            attach_data = {
                'greater_value': greater_value,
                'less_value': less_value
            }
            _allure_attach_error(attach_response=attach_data,
                                 error_name='Ошибка при сверки значений')
            raise


def assert_less_than(
        actual_value: Any,
        less_value: Any,
        allure_title: str,
        error_message: Optional[str] = None
):
    """Проверка, что одно значение меньше другого
    :param actual_value: Значение, которое проверяем
    :param less_value: Значение, которого должно быть меньше
    :param allure_title: Описание шага для allure отчета
    :param error_message: Сообщение об ошибке в случае равенства значений
    """

    with allure.step(allure_title):
        try:
            assert actual_value < less_value, error_message or f'Значение {actual_value} больше или равно {less_value}'

        except AssertionError:
            attach_data = {
                'greater_value': actual_value,
                'less_value': less_value
            }
            _allure_attach_error(attach_response=attach_data,
                                 error_name='Ошибка при сверки значений')
            raise


def _allure_attach_error(attach_response: dict, error_name: str):
    allure.attach(
        json.dumps(
            attach_response,
            indent='\t',
            separators=(',', ': '),
            ensure_ascii=False
        ),
        error_name,
        attachment_type=allure.attachment_type.JSON
    )
