import json
from typing import List

from api_testing_project.services.base_api import BaseApi
from api_testing_project.services.order.models.order_simulate_model import OrderSimulateModel, OrderLine


class ApiOrderSimulate(BaseApi):
    """API Order/Simulate"""

    def post_order_simulate(self, data: json, headers=None) -> dict:
        post_url = self.endpoints.post_order_simulate
        self.response_data = self.http_methods.post(post_url, body=data, headers=headers).json()
        return self.response_data

    @staticmethod
    def get_order_lines_object_dict(objects) -> dict:
        """Получение объекта order_lines в виде словаря"""

        order_lines = objects[0].order_lines[0]
        order_lines = order_lines.dict()
        return order_lines

    @staticmethod
    def get_order_party_object_dict(objects) -> dict:
        """Получение объекта order_party в виде словаря"""
        order_party = objects[0].order_party
        order_party = order_party.dict()
        return order_party

    def get_order_lines(self) -> OrderLine:
        """Получение объекта orderLines"""
        order_lines = self.get_objects_from_response(OrderSimulateModel)[0].order_lines[0]
        return order_lines

    def get_list_order_lines(self) -> List[OrderLine]:
        """Получение списка объекта orderLines"""
        order_lines = self.get_objects_from_response(OrderSimulateModel)[0].order_lines
        return order_lines

    def check_field_material_code_in_order_lines(self, expected_material_code: str):
        """Проверка поля materialCode в объекте order_lines"""
        self.check_for_empty_data_from_response()

        material_code_order_lines = self.get_order_lines().material_code

        assert material_code_order_lines == expected_material_code, \
            f'Значение поля materialCode в симуляции- ({material_code_order_lines}) не соответствует ожидаемому ' \
            f'полю materialCode - ({expected_material_code})'

    def check_field_description_in_order_lines(self, expected_description: str):
        """Проверка поля description в объекте order_lines"""
        self.check_for_empty_data_from_response()

        description_order_lines = self.get_order_lines().description

        assert expected_description == description_order_lines, \
            f'Значение поля description в симуляции - ({description_order_lines}) не соответствует ожидаемому ' \
            f'значению поля description - ({expected_description})'

    def check_field_weight_in_order_lines(self, expected_weight: float):
        """Проверка поля weight в объекте order_lines"""
        self.check_for_empty_data_from_response()

        weight_order_lines = self.get_order_lines().weight
        assert weight_order_lines == expected_weight, \
            f'Значение поля weight в симуляции - ({weight_order_lines}) не соответствует ожидаемому значению ' \
            f'поля weight - ({expected_weight})'

    def check_field_mpg_in_order_lines(self, expected_mpg: str):
        """Проверка поля mpg в объекте order_lines"""
        self.check_for_empty_data_from_response()

        mpg_order_lines = self.get_order_lines().mpg
        assert expected_mpg == mpg_order_lines, \
            f'Значение поля mpg в симуляции - ({mpg_order_lines}) не соответствует ожидаемому значению - ({expected_mpg})'

    def check_field_equipment_category_in_order_lines(self, expected_equipment_category: str):
        """Проверка поля equipmentCategory в объекте order_lines"""
        self.check_for_empty_data_from_response()

        equipment_category_order_lines = self.get_order_lines().equipment_category
        assert equipment_category_order_lines == expected_equipment_category, \
            f'Значение поля equipmentCategory в симуляции - ({equipment_category_order_lines}) ' \
            f'не соответствует ожидаемому значению - ({expected_equipment_category})'

    def check_field_description_in_statuses_order_lines(self, expected_description: str):
        """Проверка поля description в объекте statuses order_lines"""
        self.check_for_empty_data_from_response()
        statuses = self.get_order_lines().statuses
        description = [el.description for el in statuses]

        assert expected_description in description, \
            f'Ожидаемого описания - ({expected_description}) нет в поле description (описание) в объекте statuses' \
            f' (находится в order_lines) - ({description})'

    @staticmethod
    def checking_values_from_service_response_by_key(expected_dict: dict, response_object_dict: dict) -> dict:
        """
        Проверка значений из ответа сервиса по ключу в словаре с ожидаемыми значениями.
        Возвращает словарь с теми значениями из словаря ответа от сервиса, которые не соответствуют ожидаемым;
        expected_dict - словарь с ожидаемыми значениями
        response_object_dict - словарь с ответом от сервиса
        """
        result_assert = {}  # Словарь с результатами сравнения значений полей.
        # Сюда будут добавляться поля с ответа, значения которых не равны ожидаемым

        for key in expected_dict.keys():
            value_response = response_object_dict[key]
            if value_response != expected_dict[key]:
                print(f'{value_response} - в ответе - {key}, {expected_dict[key]} - ожидаемое- {key}')
                result_assert[key] = value_response

        return result_assert
