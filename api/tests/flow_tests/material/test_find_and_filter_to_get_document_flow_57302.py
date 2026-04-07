import allure
import pytest

from api_testing_project.services.material.api.api_find_and_filter import ApiFindAndFilter
from api_testing_project.services.material.api.api_get_material_document import ApiGetMaterialDocument
from api_testing_project.services.material.models.find_and_filter_model import FindAndFilterModel
from api_testing_project.services.material.payloads.payloads_find_and_filter import PayloadsFindAndFilter


@pytest.mark.stage
@pytest.mark.dapi
@allure.feature('DAPI')
@allure.story('Тесты на api/Material/FindAndFilter -> GetMaterialDocument')
class TestFindAndFilterToGetDocumentFlow:

    def setup_method(self):
        self.api_find_and_filter = ApiFindAndFilter()
        self.api_get_document = ApiGetMaterialDocument()

    @allure.title('Тест флоу: FindAndFilter -> GetMaterialDocument')
    @pytest.mark.stage
    @pytest.mark.parametrize('material_code, payload', [
        ('003L0145R', PayloadsFindAndFilter.request_find_and_filter_003L0145R),
        ('013G2990', PayloadsFindAndFilter.request_find_and_filter_013G2990)
    ])
    def test_find_and_filter_to_get_document_57302(self, material_code, payload):

        print(f'\n\nШАГ 1: Делаем POST запрос на api/Material/FindAndFilter')
        print(f'Ищем материал с кодом: {material_code}')

        response = self.api_find_and_filter.post_find_and_filter(payload)

        assert response.status_code == 200, \
            f'HTTP статус код - {response.status_code}, ожидался 200'
        print(f'✓ HTTP статус код: {response.status_code}')

        print(f'\nШАГ 2: Валидируем ответ через Pydantic модель')
        response_json = response.json()
        result = FindAndFilterModel(**response_json)

        status = result.status
        assert status == 'Ok', f'status в ответе - {status}, ожидался "Ok"'
        print(f'✓ Статус ответа: {status}')

        print(f'\nШАГ 3: Извлекаем список объектов')
        objects = result.objects
        assert len(objects) > 0, 'В ответе нет объектов'
        print(f'✓ Количество объектов в ответе: {len(objects)}')

        print(f'\nШАГ 4: Получаем документы из первого объекта')
        first_object = objects[0]
        documents = first_object.documents
        print(f'✓ Количество документов: {len(documents)}')

        print(f'\nШАГ 5: Фильтруем документы (пропускаем "Письмо о замене")')
        valid_documents = [
            doc for doc in documents
            if doc.type != "Письмо о замене" and doc.title is not None
        ]
        print(f'✓ Количество валидных документов: {len(valid_documents)}')

        assert len(valid_documents) > 0, \
            'Нет валидных документов с title для скачивания'

        print(f'\nШАГ 6: Выбираем первый документ для скачивания')
        document_to_download = valid_documents[0]
        print(f'  Тип документа: {document_to_download.type}')
        print(f'  Название файла: {document_to_download.title}')

        print(f'\nШАГ 7: Делаем GET запрос на api/Material/GetMaterialDocument')
        response_get = self.api_get_document.get_material_document(
            material_code=material_code,
            file_name=document_to_download.title
        )

        assert response_get.status_code == 200, \
            f'HTTP статус код GetMaterialDocument - {response_get.status_code}, ожидался 200'
        print(f'✓ HTTP статус код GetMaterialDocument: {response_get.status_code}')

        print(f'\nШАГ 8: Проверяем, что файл успешно скачался')
        assert len(response_get.content) > 0, \
            'Файл не содержит данных (content пустой)'
        print(f'✓ Размер скачанного файла: {len(response_get.content)} байт')

        print(f'\n✓ Тест успешно завершен!')
        print(f'  Материал: {material_code}')
        print(f'  Документ: {document_to_download.title}')
        print(f'  Размер: {len(response_get.content)} байт')