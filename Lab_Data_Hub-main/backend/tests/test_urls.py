import uuid

import pytest
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from api.models import User


@pytest.mark.django_db(transaction=True)
class TestAPIEndpoints:

    @classmethod
    def setup_class(cls):
        cls.client = APIClient()

    def create_test_user(self, username):
        return User.objects.create_user(username=username,
                                        password='Testpassword')

    def test_list_endpoint(self):
        """Проверяем все эндпоинты."""
        username = 'testuser_lab'
        user = self.create_test_user(username)
        self.client.force_authenticate(user=user)
        urls = [
            '/api/labs/',
            '/api/tests/',
            '/api/indicators/',
            '/api/metrics/',
            '/api/indicator-metrics/',
            '/api/scores/',
            '/api/references/',
            '/api/test-results/'
        ]
        for url in urls:
            response = self.client.get(url)
            assert response.status_code != 404, f'Страница `{url}` не найдена'
            assert response.status_code == 200, (
                f'Ошибка {response.status_code} при запросе `{url}`')

    def test_create_lab_endpoint(self):
        """Проверяем эндпоинт для создания новой лаборатории."""
        username = 'testuser_lab'
        user = self.create_test_user(username)
        self.client.force_authenticate(user=user)
        url = '/api/labs/'
        lab_id = str(uuid.uuid4())
        data = {
            'id': lab_id,
            'name': 'Новая лаборатория',
            'is_active': True,
            'created_at': timezone.now(),
            'updated_at': timezone.now()
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED, (
            f'Ошибка при создании лаборатории {url}')
        lab_id = response.json()['id']
        return lab_id

    def test_create_test_endpoint(self):
        """Проверяем эндпоинт для создания нового теста"""
        lab_id = self.test_create_lab_endpoint()
        test_id = str(uuid.uuid4())
        url = '/api/tests/'
        data = {
            'id': test_id,
            'started_at': timezone.now(),
            'completed_at': timezone.now(),
            'comment': 'Test',
            'is_active': True,
            'created_at': timezone.now(),
            'updated_at': timezone.now(),
            'lab_id': lab_id
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED, (
            f'Ошибка при создании теста {url}')
        test_id = response.json()['id']
        return test_id

    def test_create_indicators_endpoint(self):
        """Проверяем эндпоинт для создания нового показателя"""
        indicator_id = str(uuid.uuid4())
        url = '/api/indicators/'
        data = {
            'id': indicator_id,
            'name': 'indicator_name',
            'description': 'description_indicator',
            'is_active': True,
            'created_at': timezone.now(),
            'updated_at': timezone.now(),
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED, (
            f'Ошибка при создании показателя {url}')
        indicator_id = response.json()['id']
        return indicator_id

    def test_create_metrics_endpoint(self):
        """Проверяем эндпоинт для создания новой метрики"""
        metric_id = str(uuid.uuid4())
        url = '/api/metrics/'
        data = {
            'id': metric_id,
            'name': 'metric_name',
            'description': 'metric_description',
            'unit': 'metric_unit',
            'is_active': True,
            'created_at': timezone.now(),
            'updated_at': timezone.now(),
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED, (
            f'Ошибка при создании метрики {url}')
        metrics_id = response.json()['id']
        return metrics_id

    def test_create_indicator_metrics_endpoint(self):
        """Проверяем эндпоинт для создания нового показателя метрики."""
        indicator_metric_id = str(uuid.uuid4())
        indicator_id = self.test_create_indicators_endpoint()
        metric_id = self.test_create_metrics_endpoint()
        url = '/api/indicator-metrics/'
        data = {
            'id': indicator_metric_id,
            'is_active': True,
            'created_at': timezone.now(),
            'updated_at': timezone.now(),
            'indicator_id': indicator_id,
            'metric_id': metric_id,
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED, (
            f'Ошибка при создании оказателя метрики {url}')
        indicator_metric_id = response.json()['id']
        return indicator_metric_id

    def test_create_score_endpoint(self):
        """Проверяем эндпоинт для создания нового количественного значения."""
        score_id = str(uuid.uuid4())
        indicator_metric_id = self.test_create_indicator_metrics_endpoint()
        test_id = self.test_create_test_endpoint()
        current_time = timezone.now()
        url = '/api/scores/'
        data = {
            'id': score_id,
            'score': '10',
            'created_at': current_time,
            'updated_at': current_time,
            'test_id': test_id,
            'indicator_metric_id': indicator_metric_id
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED, (
            f'Ошибка при создании количественного значения {url}')
        score_id = response.json()['id']
        return score_id

    def test_create_reference_endpoint(self):
        """Проверяем эндпоинт для создания новой справки."""
        reference_id = str(uuid.uuid4())
        indicator_metric_id = self.test_create_indicator_metrics_endpoint()
        url = '/api/references/'
        data = {
            'id': reference_id,
            'min_score': '10',
            'max_score': '10',
            'created_at': timezone.now(),
            'updated_at': timezone.now(),
            'indicator_metric_id': indicator_metric_id
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED, (
            f'Ошибка при создании количественного значения {url}')
        reference_id = response.json()['id']
        return reference_id

    def test_create_user_endpoint(self):
        """Проверяем эндпоинт для создания нового пользователя."""

        url = '/api/users/'
        data = {
            'email': 'User_mail@mail.ru',
            'username': 'Username',
            'password': 'Qweasdf1234'
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED, (
            f'Ошибка при создании нового пользователя {url}')

    def test_get_lab_by_id(self):
        """Проверяем эндпоинт для получения лаборатории по ID."""
        lab_id = self.test_create_lab_endpoint()
        url = f'/api/labs/{lab_id}/'
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK, (
            f'Ошибка при получении лаборатории по ID {url}')
        lab = response.json()
        assert lab['id'] == lab_id, 'ID лаборатории не совпадает'

    def test_delete_lab_by_id(self):
        """Проверяем эндпоинт для удаления лаборатории по ID."""
        lab_id = self.test_create_lab_endpoint()
        url = f'/api/labs/{lab_id}/'
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT, (
            f'Ошибка при удалении лаборатории по ID {url}')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND, (
            'Лаборатория не удалена')

    def test_get_test_by_id(self):
        """Проверяем эндпоинт для получения теста по ID."""
        test_id = self.test_create_test_endpoint()
        url = f'/api/tests/{test_id}/'
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK, (
            f'Ошибка при получении теста по ID {url}')
        test = response.json()
        assert test['id'] == test_id, 'ID теста не совпадает'

    def test_delete_test_by_id(self):
        """Проверяем эндпоинт для удаления теста по ID."""
        test_id = self.test_create_test_endpoint()
        url = f'/api/tests/{test_id}/'
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT, (
            f'Ошибка при удалении теста по ID {url}')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND, (
            'Тест не удален')

    def test_get_indicator_by_id(self):
        """Проверяем эндпоинт для получения показателя по ID."""
        indicator_id = self.test_create_indicators_endpoint()
        url = f'/api/indicators/{indicator_id}/'
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK, (
            f'Ошибка при получении показателя по ID {url}')
        indicator = response.json()
        assert indicator['id'] == indicator_id, 'ID показателя не совпадает'

    def test_delete_indicator_by_id(self):
        """Проверяем эндпоинт для удаления показателя по ID."""
        indicator_id = self.test_create_indicators_endpoint()
        url = f'/api/indicators/{indicator_id}/'
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT, (
            f'Ошибка при удалении показателя по ID {url}')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND, (
            'Показатель не удален')

    def test_get_metric_by_id(self):
        """Проверяем эндпоинт для получения метрики по ID."""
        metric_id = self.test_create_metrics_endpoint()
        url = f'/api/metrics/{metric_id}/'
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK, (
            f'Ошибка при получении метрики по ID {url}')
        metric = response.json()
        assert metric['id'] == metric_id, 'ID метрики не совпадает'

    def test_delete_metric_by_id(self):
        """Проверяем эндпоинт для удаления метрики по ID."""
        metric_id = self.test_create_metrics_endpoint()
        url = f'/api/metrics/{metric_id}/'
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT, (
            f'Ошибка при удалении метрики по ID {url}')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND, (
            'Метрика не удалена')

    def test_get_indicator_metric_by_id(self):
        """Проверяем эндпоинт для получения показателя метрики по ID."""
        indicator_metric_id = self.test_create_indicator_metrics_endpoint()
        url = f'/api/indicator-metrics/{indicator_metric_id}/'
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK, (
            f'Ошибка при получении показателя метрики по ID {url}')
        indicator_metric = response.json()
        assert indicator_metric['id'] == indicator_metric_id, (
            'ID показателя метрики не совпадает')

    def test_delete_indicator_metric_by_id(self):
        """Проверяем эндпоинт для удаления показателя метрики по ID."""
        indicator_metric_id = self.test_create_indicator_metrics_endpoint()
        url = f'/api/indicator-metrics/{indicator_metric_id}/'
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT, (
            f'Ошибка при удалении показателя метрики по ID {url}')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND, (
            'Показатель метрики не удален')

    def test_get_score_by_id(self):
        """Проверяем эндпоинт для получения количественного значения по ID."""
        score_id = self.test_create_score_endpoint()
        url = f'/api/scores/{score_id}/'
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK, (
            f'Ошибка при получении количественного значения по ID {url}')
        score = response.json()
        assert score['id'] == score_id, (
            'ID количественного значения не совпадает')

    def test_delete_score_by_id(self):
        """Проверяем эндпоинт для удаления количественного значения по ID."""
        score_id = self.test_create_score_endpoint()
        url = f'/api/scores/{score_id}/'
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT, (
            f'Ошибка при удалении количественного значения по ID {url}')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND, (
            'Количественное значение не удалено')

    def test_get_reference_by_id(self):
        """Проверяем эндпоинт для получения справки по ID."""
        reference_id = self.test_create_reference_endpoint()
        url = f'/api/references/{reference_id}/'
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK, (
            f'Ошибка при получении справки по ID {url}')
        reference = response.json()
        assert reference['id'] == reference_id, 'ID справки не совпадает'

    def test_delete_reference_by_id(self):
        """Проверяем эндпоинт для удаления справки по ID."""
        reference_id = self.test_create_reference_endpoint()
        url = f'/api/references/{reference_id}/'
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT, (
            f'Ошибка при удалении справки по ID {url}')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND, (
            'Справка не удалена')

    def test_get_test_results_for_lab(self):
        """Проверяем фильтрацию результатов тестов по ID лаборатории."""
        lab_id = self.test_create_lab_endpoint()
        url = f'/api/test-results/?lab_id={lab_id}'
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK, (
            f'Ошибка при получении результатов тестов для лаборатории {url}')
        test_results = response.json()
        for result in test_results:
            assert result['test']['lab_id'] == lab_id, (
                'ID лаборатории не совпадает с ожидаемым')

    def test_delete_test_results_for_lab(self):
        """Проверяем удаление результатов тестов по ID лаборатории."""
        user = User.objects.create(
            username='testuser', password='testpassword')
        self.client.force_authenticate(user=user)
        test_id = self.test_create_test_endpoint()
        url = f'/api/test-results/{test_id}/'
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT, (
            f'Ошибка при удалении справки по ID {url}')
        response = self.client.get(url)
        assert (response.status_code == status.HTTP_404_NOT_FOUND) or (
            response.status_code == status.HTTP_200_OK and response.data.get(
                "lab_id") is None), (
            'Справка не удалена')
