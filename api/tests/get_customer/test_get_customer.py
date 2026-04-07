import allure
import pytest

from api_testing_project.services.customer.models.get_customer_by_inn_model import GetCustomerByInn
from api_testing_project.services.customer.models.get_customer_by_number_model import GetCustomerByNumber
from api_testing_project.services.customer.models.get_customer_model import GetCustomer
from api_testing_project.services.customer.payloads.payloads import Payloads


@pytest.mark.stage
@pytest.mark.dapi
@allure.feature('DAPI')
@allure.story('Позитивные тесты на API GetCustomer')
class TestGetCustomerSuite:
    """Позитивные тесты на API GetCustomer"""

    @allure.title('Позитивный тест на API GetCustomer')
    @pytest.mark.stage
    @pytest.mark.parametrize('debtor_account', [Payloads.debtor_account_vodokomfort])
    def test_get_customer(self, debtor_account, setup_customer_api):
        """Позитивный тест на API GetCustomer"""

        print('\nДелаем запрос на GetCustomer')

        response_get_customer = setup_customer_api.get_customer(debtor_account)

        response_json = response_get_customer.json()

        result = GetCustomer(**response_json)

        status = result.status
        assert status == 'Ok', f'status в ответе не Ок - {status}'

    @allure.title('Позитивный тест на API GetCustomerByInn')
    @pytest.mark.stage
    @pytest.mark.parametrize('inn', [Payloads.inn_vodokomfort])
    def test_get_customer_by_inn(self, inn, setup_customer_api):
        print('Делаем запрос на GetCustomerByInn по ИНН')

        response_get_customer_by_inn = setup_customer_api.get_customer_by_inn(inn)
        response_json_by_inn = response_get_customer_by_inn.json()

        res_get_customer_by_inn = GetCustomerByInn(**response_json_by_inn)

        status = res_get_customer_by_inn.status
        assert status == 'Ok', f'status в ответе не Ок - {status}'

    @allure.title('Позитивный тест на API GetCustomerByInn')
    @pytest.mark.stage
    @pytest.mark.parametrize('debtor_account', [Payloads.debtor_account_for_get_customer_by_number])
    def test_get_customer_by_number(self, debtor_account, setup_customer_api):
        print('Делаем запрос на GetCustomerByNumber по ИНН')
        response_get_customer_by_number = setup_customer_api.get_customer_by_number(debtor_account)
        response_json_by_number = response_get_customer_by_number.json()
        res_get_customer_by_number = GetCustomerByInn(**response_json_by_number)

        status = res_get_customer_by_number.status
        assert status == 'Ok', f'status в ответе не Ок - {status}'

    @allure.title('Позитивный тест на API GetCustomer, GetCustomerByInn, GetCustomerByNumber')
    @pytest.mark.stage
    @pytest.mark.parametrize('debtor_account', [Payloads.debtor_account_vodokomfort])
    def test_get_customer_all(self, debtor_account, setup_customer_api):
        """Позитивный тест на API GetCustomer, GetCustomerByInn, GetCustomerByNumber.
        Делаем запрос на GetCustomer, получаем оттуда ИНН и Название компании ->
        По полученному ИНН делаем запрос на getCustomerByInn, сохраняем Название компании в ответе, сверяем с названием
        компании из ответа от GetCustomer. Сохраняем debtorAccount ->
        Делаем запрос в getCustomerByNumber по сохраненному debtorAccount. Также сверяем в ответе поле publicName с
        полем name в ответе GetCustomer
        """

        print('\nДелаем запрос на GetCustomer')
        response_get_customer = setup_customer_api.get_customer(debtor_account)

        response_json = response_get_customer.json()
        result = GetCustomer(**response_json)

        print('Получаем ИНН')
        objects = result.objects
        inn = objects[0].inn
        print(inn, '- inn in response GetCustomer')

        # Делаем запрос на GetCustomerByInn по полученному ИНН
        print('Делаем запрос на GetCustomerByInn по полученному ИНН')
        response_get_customer_by_inn = setup_customer_api.get_customer_by_inn(inn)
        response_json_by_inn = response_get_customer_by_inn.json()
        res_get_customer_by_inn = GetCustomerByInn(**response_json_by_inn)
        objects_by_inn = res_get_customer_by_inn.objects  # Получаем объект objects из ответа

        inn_get_customer_by_inn = objects_by_inn[0].inn
        print(inn_get_customer_by_inn, ' - inn in response GetCustomerByInn')
        assert inn_get_customer_by_inn == inn, \
            f'В ответе GetCustomerByInn значение поля inn - {inn_get_customer_by_inn} не соответствует ' \
            f'ожидаемому полю inn в ответе GetCustomer- {inn}'

        debtor_account_for_get_customer_by_number = objects_by_inn[0].debtorAccount.strip()

        # Делаем запрос на GetCustomerByNumber по полученному debtorAccount
        response_get_customer_by_number = setup_customer_api.get_customer_by_number(
            debtor_account_for_get_customer_by_number)
        response_json_by_number = response_get_customer_by_number.json()
        res_get_customer_by_number = GetCustomerByNumber(**response_json_by_number)
        objects_by_number = res_get_customer_by_number.objects  # Получаем объект objects из ответа

        inn_get_customer_by_number = objects_by_number[0].inn
        assert inn_get_customer_by_number == inn, \
            f'В ответе GetCustomerByNumber значение поля inn - {inn_get_customer_by_number} не соответствует ' \
            f'ожидаемому полю inn в ответе GetCustomer- {inn}'


@pytest.mark.stage
@pytest.mark.dapi
@allure.feature('DAPI')
@allure.story('Негативные тесты на GetCustomer')
class TestGetCustomerSuiteNegative:
    """Негативные тесты на GetCustomer"""

    @allure.title('GetCustomer')
    @pytest.mark.stage
    @pytest.mark.parametrize('debtor_account, expected_messages', [
        ('001440384', 'Не найден клиент по указаному номеру'),
        ('qwe', 'Не найден клиент по указаному номеру'),
        ('_123_', 'Не найден клиент по указаному номеру'),
        ('@!&^*()', 'Не найден клиент по указаному номеру'),
        ('asd!#$%&^&__132', 'Не найден клиент по указаному номеру'),
        ('<b>', 'Не найден клиент по указаному номеру'),
        (' ', 'Необходимо указать номер клиента.')])
    def test_negative_get_customer(self, debtor_account, expected_messages, setup_customer_api):
        """Негативный тест на API GetCustomer"""

        response = setup_customer_api.get_customer(debtor_account)

        response_json = response.json()
        result = GetCustomer(**response_json)

        messages_text = ' '.join(result.messages)
        assert messages_text == expected_messages, \
            f'Текст - ({messages_text}) в поле {list(result.__annotations__.keys())[1]} ' \
            f'не соответствует ожидаемому - ({expected_messages})'

    @allure.title('GetCustomerByInn')
    @pytest.mark.stage
    @pytest.mark.parametrize('inn', ['12354', '!@##12', 'asdsad', '<br>', '(*&(*asd123', ' '])
    def test_negative_get_customer_by_inn(self, inn, setup_customer_api):
        """Негативный тест на API GetCustomerByInn"""
        response = setup_customer_api.get_customer_by_inn(inn)
        response_json = response.json()
        result = GetCustomerByInn(**response_json)

        status = result.status
        assert status == 'Ok' or status == 'Error', \
            f'Статус в ответе - {status} не соответствует ожидаемому - Ok или Error'

    @allure.title('GetCustomerByNumber')
    @pytest.mark.stage
    @pytest.mark.parametrize('debtor_account', ['12354  _', '!@##12', 'asdsad', '<br>', '(*&(*asd123', ' '])
    def test_negative_get_customer_by_number(self, debtor_account, setup_customer_api):
        """Негативный тест на API GetCustomerByNumber"""

        response = setup_customer_api.get_customer_by_number(debtor_account)
        response_json = response.json()
        result = GetCustomerByNumber(**response_json)

        status = result.status
        assert status == 'Ok' or 'Error', f'Статус в ответе - {status} не соответствует ожидаемому - Ok'
