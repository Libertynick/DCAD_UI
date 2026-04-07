import allure
import pytest
from api_testing_project.db_sheduler_stg.db_sheduler_stg import DatabaseConnection
from api_testing_project.services.material.api.api_update_materials import ApiUpdateMaterials
from api_testing_project.services.material.payloads.payloads import PayloadsUpdateMaterial
from api_testing_project.services.order.api.api_order_simulate import ApiOrderSimulate


@pytest.mark.stage
@pytest.mark.dapi
@allure.feature('DAPI')
@allure.story('test for api/Material/UpdateMaterials')
class TestUpdateMaterials:
    """test for api/Material/UpdateMaterials"""

    @allure.title('Тест на api/Material/UpdateMaterials. Добавление и редактирование артикула')
    @pytest.mark.parametrize('payload_update_materials, payloads_order_simulate',
                             [
                                 (PayloadsUpdateMaterial.create_material, PayloadsUpdateMaterial.add_to_cart_code),
                                 (PayloadsUpdateMaterial.update_material, PayloadsUpdateMaterial.add_to_cart_code)
                             ]
                             )
    def test_update_materials_added_and_editing_article(self, payload_update_materials, payloads_order_simulate):
        """Тест на api/Material/UpdateMaterials. Добавление и редактирование артикула"""
        api_update_material = ApiUpdateMaterials()
        api_update_material.post_update_materials(payload_update_materials)
        material_number = payload_update_materials[0]['MaterialNumber']  # Код материала в запросе
        print(f'\n{material_number} - артикул для создания и редактирования')

        query_select_for_db = f"SELECT * FROM [db_scheduler_stg].[dbo].[sl_tbl_Assortments] " \
                              f"WHERE sapMaterialCode = '{material_number}'"

        db = DatabaseConnection()
        db.connect()
        tbl_assortments = db.execute_query(query_select_for_db)[0]
        db.close()

        # Проверяем значение полей в запросе со значениями полей из таблицы [sl_tbl_Assortments]

        # Ожидаемые значения полей. Берем из запроса updateMaterial
        expected_code = payload_update_materials[0]['MaterialNumber']
        expected_description = payload_update_materials[0]['Description']
        expected_weight = float(payload_update_materials[0]['Weight'])
        expected_ware_house_category = payload_update_materials[0]['WareHouseCategory']
        expected_price_category = payload_update_materials[0]['PriceCategory']
        expected_equipment_category = payload_update_materials[0]['EquipmentCategory']

        # Значения полей из таблицы [sl_tbl_Assortments]
        ware_house_category_tbl_assortments = tbl_assortments['WareHouseCategory']
        sap_material_code_tbl_assortments = tbl_assortments['sapMaterialCode']
        name_tbl_assortments = tbl_assortments['name']
        mass_tbl_assortments = float(tbl_assortments['mass'])

        assert sap_material_code_tbl_assortments == expected_code, \
            f'Код в запросе на update_materials ({expected_code}) не соответствует коду в таблице ' \
            f'tbl_assortments - ({sap_material_code_tbl_assortments})'

        assert expected_description == name_tbl_assortments, \
            f'Ожидаемое значение поля description из запроса - ({expected_description}) не соответствует значению ' \
            f'поля name из таблицы tbl_assortments - ({name_tbl_assortments})'

        assert expected_weight == mass_tbl_assortments, \
            f'Ожидаемая масса из запроса в поле Weight - ({expected_weight}) не равна массе в таблице ' \
            f'tbl_assortments - ({mass_tbl_assortments})'

        assert expected_ware_house_category == ware_house_category_tbl_assortments, \
            f'Ожидаемая WareHouseCategory в запросе - ({expected_ware_house_category}) ' \
            f'не соответствует WareHouseCategory в таблице tbl_assortments - ({ware_house_category_tbl_assortments})'

        # Сверяем информацию в запросе с информацией в ответе order/simulate (добавление в корзину товара)
        api_order_simulate = ApiOrderSimulate()
        api_order_simulate.post_order_simulate(payloads_order_simulate)

        api_order_simulate.check_field_material_code_in_order_lines(expected_code)
        api_order_simulate.check_field_description_in_order_lines(expected_description)
        api_order_simulate.check_field_weight_in_order_lines(expected_weight)
        api_order_simulate.check_field_mpg_in_order_lines(expected_price_category)
        api_order_simulate.check_field_equipment_category_in_order_lines(expected_equipment_category)

    @allure.title('Тест на api/Material/UpdateMaterials. Удаление артикула')
    @pytest.mark.parametrize('payload_delete_materials, payloads_order_simulate',
                             [
                                 (PayloadsUpdateMaterial.delete_material, PayloadsUpdateMaterial.add_to_cart_code)
                             ]
                             )
    @pytest.mark.skip(reason='Не актуален. Материал не добавляется в папку удаления')
    def test_delete_article(self, payload_delete_materials, payloads_order_simulate):
        """Тест на api/Material/UpdateMaterials. Удаление артикула"""
        path_to_folder_delete_article = 'CE1B0E09-4499-4DA3-9C53-247C3CA87B72'  # путь к папке, в которой хранятся удаленные коды

        api_update_material = ApiUpdateMaterials()
        api_update_material.post_update_materials(payload_delete_materials)
        material_number = payload_delete_materials[0]['MaterialNumber']  # Код материала в запросе
        print(f'\n{material_number} - артикул для удаления')

        query_select_for_db = f"SELECT * FROM [db_scheduler_stg].[dbo].[sl_tbl_Assortments] " \
                              f"WHERE sapMaterialCode = '{material_number}'"

        db = DatabaseConnection()
        db.connect()
        tbl_assortments = db.execute_query(query_select_for_db)[0]
        db.close()

        # Значения полей из таблицы [sl_tbl_Assortments]
        parent_id_tbl_assortments = tbl_assortments['ParentId']  # путь к папке, в которую помещаются удаленные артикулы
        assert parent_id_tbl_assortments == path_to_folder_delete_article, \
            f'Удаленный код - ({material_number}) не поместился в папку удаленных кодов - ({path_to_folder_delete_article})'

        # Делаем запрос в order/simulate. Сверяем описание кода в ответе
        expected_description_simulate = 'Материал не найден'

        api_order_simulate = ApiOrderSimulate()
        api_order_simulate.post_order_simulate(payloads_order_simulate)
        api_order_simulate.check_field_description_in_statuses_order_lines(expected_description_simulate)

    @allure.title('Тест на api/Material/UpdateMaterials. Блокировка артикула')
    @pytest.mark.parametrize('payload_blocked_materials, payloads_order_simulate',
                             [
                                 (PayloadsUpdateMaterial.blocked_material, PayloadsUpdateMaterial.add_to_cart_code)
                             ]
                             )
    def test_blocked_article(self, payload_blocked_materials, payloads_order_simulate):
        """Тест на api/Material/UpdateMaterials. Блокировка артикула"""
        path_to_folder_blocked_article = 'EE5786BF-4D4D-43A1-A757-731C9A944206'  # путь к папке, в которой хранятся заблокированные коды

        api_update_material = ApiUpdateMaterials()
        api_update_material.post_update_materials(payload_blocked_materials)
        material_number = payload_blocked_materials[0]['MaterialNumber']  # Код материала в запросе
        print(f'\n{material_number} - артикул для блокировки')

        query_select_for_db = f"SELECT * FROM [db_scheduler_stg].[dbo].[sl_tbl_Assortments] " \
                              f"WHERE sapMaterialCode = '{material_number}'"

        db = DatabaseConnection()
        db.connect()
        tbl_assortments = db.execute_query(query_select_for_db)[0]
        db.close()

        # Значения полей из таблицы [sl_tbl_Assortments]
        lock_code_id = tbl_assortments['lockCodeId']  # путь к папке, в которую помещаются заблокированные артикулы
        assert lock_code_id == path_to_folder_blocked_article, \
            f'Заблокированный код - ({material_number}) не поместился в папку удаленных кодов - ({path_to_folder_blocked_article})'

        # Делаем запрос в order/simulate. Сверяем описание кода в ответе
        expected_description_simulate = 'Материал заблокирован для сбыта'

        api_order_simulate = ApiOrderSimulate()
        api_order_simulate.post_order_simulate(payloads_order_simulate)
        api_order_simulate.check_field_description_in_statuses_order_lines(expected_description_simulate)
