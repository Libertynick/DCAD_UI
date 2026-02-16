
import allure
import pytest

from base_page.base_page import BasePage
from dcad_pages.tdu_config_2_page.tdu_config_2 import TduListPage
from tools.routes.dcad_routes import DcadRoutes
from config import TestEnvironment


@allure.feature('DCAD тесты')
@allure.story('Конфигуратор TDU - Проверка фильтров и результатов')
@pytest.mark.parametrize(
    "node_type, branches, riser, inlet_diameter, partner_valve, branch_valves, expected_count, expected_articles",
    [
        # Тест 1: TDU.7R, 2 отвода, Слева, 20мм, Есть партнер, MVT-R
        (
                "TDU.7R",  # Тип узла
                "2",  # Количество отводов
                "Слева",  # Стояк
                "20",  # Ду ввода
                "Есть",  # Клапан-партнёр
                "MVT-R",  # Клапаны на отводах
                2,  # Ожидаемое количество результатов
                ["TDU0010121", "TDU0014348"]  # Ожидаемые артикулы
        ),
        # Можно добавить больше наборов параметров:
        # ("TDU.5R", "3", "Справа", "25", "Нет", "MVT-R LF", 1, ["TDU0015555"]),
    ],
    ids=[
        "TDU7R_2отвода_Слева_20_Есть_MVTR",
        # Добавь id для каждого набора параметров
    ]
)
@pytest.mark.stage
def test_tdu_config_filters_and_results(
        browser,
        authorization_dcad_fixture,
        node_type,
        branches,
        riser,
        inlet_diameter,
        partner_valve,
        branch_valves,
        expected_count,
        expected_articles
):
    """
    Тест проверки фильтров TDU Config 2 Page и результатов поиска

    Шаги:
    1. Авторизация в DCAD
    2. Открыть страницу Конфигуратор TDU
    3. Установить фильтры (каждый отдельно)
    4. Проверить количество результатов в таблице
    5. Проверить наличие ожидаемых артикулов
    """

    login = TestEnvironment.DCAD_LOGIN
    password = TestEnvironment.DCAD_PASSWORD

    page_main = BasePage(browser, DcadRoutes.PAGE_AUTHORIZATION)
    page_main.open()

    authorization_dcad_fixture(login, password)

    page_tdu_list = TduListPage(browser, DcadRoutes.PAGE_CONFIG_2)

    page_tdu_list.open()
    page_tdu_list.should_header_page_visible()

    # Устанавливаем фильтры
    page_tdu_list.filter_component.select_node_type(node_type)
    page_tdu_list.filter_component.select_branches(branches)
    page_tdu_list.filter_component.select_riser(riser)
    page_tdu_list.filter_component.select_inlet_diameter(inlet_diameter)
    page_tdu_list.filter_component.select_partner_valve(partner_valve)
    page_tdu_list.filter_component.select_branch_valves(branch_valves)

    # Проверяем что таблица результатов отобразилась
    page_tdu_list.results_table_component.should_table_title_visible()

    # Проверяем кол-во результатов
    page_tdu_list.results_table_component.check_results_count(expected_count)

    # Проверяем артикулы
    for article in expected_articles:
        page_tdu_list.results_table_component.check_table_contains_article(article)
