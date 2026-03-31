import os
import pytest
from tools.routes.dcad_routes import DcadRoutes


@pytest.fixture(scope='session')
def dcad_env(request):
    env = request.config.getoption('--env')

    if env == 'prod':
        base_url = os.getenv('DCAD_URL_PROD')
        login = os.getenv('DCAD_LOGIN_PROD')
        password = os.getenv('DCAD_PASSWORD_PROD')
    else:
        base_url = os.getenv('DCAD_URL_STAGE')
        login = os.getenv('DCAD_LOGIN')
        password = os.getenv('DCAD_PASSWORD')

    return {
        'login': login,
        'password': password,
        'routes': DcadRoutes(base_url)
    }


@pytest.fixture(scope='session', autouse=True)
def allure_environment(request, dcad_env):
    env = request.config.getoption('--env')
    allure_dir = 'allure_res'

    if env == 'prod':
        url = os.getenv('DCAD_URL_PROD')
    else:
        url = os.getenv('DCAD_URL_STAGE')

    if os.path.exists(allure_dir):
        with open(f'{allure_dir}/environment.properties', 'w', encoding='utf-8') as f:
            f.write(f'Environment={env}\n')
            f.write(f'URL={url}\n')