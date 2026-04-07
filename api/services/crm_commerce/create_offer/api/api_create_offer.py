import json

from api_testing_project.services.base_api import BaseApi
from api_testing_project.services.crm_commerce.create_offer.models.create_offer_model import ResponseModel, Offer, Line
from api_testing_project.services.endpoints import Endpoints


class ApiCreateOffer(BaseApi):
    """/api/CrmCommerce/CreateOffer"""

    def post_create_offer(self, data: json, headers=None):
        """Запрос Post на  /api/CrmCommerce/CreateOffer"""
        post_url = Endpoints.post_create_offer
        self.response_data = self.http_methods.post(url=post_url, body=data, headers=headers).json()

        return self.response_data

    def create_offer(self, request: json, headers: dict[str, str] = None) -> tuple:
        """
        Создание КП через срм в статусе Черновик.
        Возвращает id созданного КП и его номер в кортеже
        :param headers: Заголовки запроса
        :param request: Запрос
        :return: (id_offers, num_pq)
        """

        self.post_create_offer(data=request, headers=headers)
        id_offers = self.get_id_from_object_offers()
        num_pq = self.get_number_from_object_offers()
        print(f'{id_offers}  offer_id')
        print(f'Номер КП {num_pq} при создании через api_create_offer ')
        return id_offers, num_pq

    def get_object_offers(self) -> Offer:
        """Получение объекта offers"""
        self.check_for_empty_data_from_response()

        offers = self.get_objects_from_response(ResponseModel)[0].offers
        return offers

    def get_object_lines(self) -> Line:
        """
        Получение объекта lines
        :return: Объект lines
        """
        self.check_for_empty_data_from_response()

        lines = self.get_objects_from_response(ResponseModel)[0].lines
        return lines

    def get_id_from_object_offers(self):
        """Получение id из объекта offers"""
        id_offers = self.get_object_offers()[0].id
        return id_offers

    def get_number_from_object_offers(self):
        """Получение поля number из объекта offers"""
        number = self.get_object_offers()[0].number
        return number

    def get_all_number_from_object_offers(self) -> list[str]:
        """Получение списка всех значений поля number из объекта offers"""
        offers = self.get_object_offers()
        number_list = []
        for offer in offers:
            number_list.append(offer.number)

        return number_list

    def get_all_articles(self):
        """
        Получение всех артикулов в заказе
        :return: Список артикулов
        """
        lines = self.get_object_lines()
        article = [line.code for line in lines]

        return article

    def post_create_offer_with_user_id(self, data: json, user_id: str = None, headers=None):
        """
        Запрос Post на /api/CrmCommerce/CreateOffer с userId в query параметрах
        """
        post_url = Endpoints.post_create_offer

        # Если передан userId, добавляем его в URL как query параметр
        if user_id:
            post_url = f"{post_url}?userId={user_id}"

        # КРИТИЧЕСКИ ВАЖНЫЙ DEBUG:
        print(f"\n🔍 DEBUG: Финальный URL = {post_url}")
        print(f"🔍 DEBUG: userId передан = {user_id}")

        self.response_data = self.http_methods.post(url=post_url, body=data, headers=headers).json()
        return self.response_data
