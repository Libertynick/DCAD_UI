import pytest

from api_testing_project.services.customer.api.api_customer import CustomerApi


@pytest.fixture(scope='function')
def setup_customer_api():
    """Фикстура для инициализации CustomerApi"""
    customer_api = CustomerApi()
    return customer_api
