import allure

from api_testing_project.services.base_api import BaseApi


class CustomerApi(BaseApi):
    """API GetCustomer"""

    def get_customer(self, debtor_account: str):
        """API GetCustomer"""
        with allure.step('GET. GetCustomer'):
            get_url = self.endpoints.get_customer(debtor_account)
            print(f'URL GetCustomer  {get_url}')
            res_get = self.http_methods.get(url=get_url)
            return res_get

    def get_customer_by_inn(self, inn: str):
        """API GetCustomerByInn"""
        with allure.step('GET. GetCustomerByInn'):
            get_url = self.endpoints.get_customer_by_inn(inn)
            print(f'URL GetCustomerByInn  {get_url}')
            res_get = self.http_methods.get(url=get_url)
            return res_get

    def get_customer_by_number(self, debtor_account: str):
        """API GetCustomerByNumber"""
        with allure.step('GET. GetCustomerByNumber'):
            get_url = self.endpoints.get_customer_by_number(debtor_account)
            print(f'URL GetCustomerByNumber  {get_url}')
            res_get = self.http_methods.get(url=get_url)
            return res_get

