import pytest
from django.utils import timezone

from api.models import (IndicatorMetric, Indicators, Labs, Metrics, Reference,
                        Scores, Tests)


@pytest.fixture
def lab_data():
    return {
        'name': 'Лаборатория 1',
        'is_active': True,
        'created_at': timezone.now(),
        'updated_at': timezone.now(),
    }


@pytest.fixture
def test_data(lab_data):
    return {
        'started_at': timezone.now(),
        'completed_at': timezone.now(),
        'comment': 'Комментарий к тесту',
        'lab_id': Labs.objects.create(**lab_data),
        'is_active': True,
        'created_at': timezone.now(),
        'updated_at': timezone.now(),
    }


@pytest.fixture
def indicator_data():
    return {
        'name': 'Показатель 1',
        'description': 'Описание 1',
        'is_active': True,
        'created_at': timezone.now(),
        'updated_at': timezone.now(),
    }


@pytest.fixture
def metric_data():
    return {
        'name': 'Метрика 1',
        'description': 'Описание 1',
        'unit': 'Единица измерения 1',
        'is_active': True,
        'created_at': timezone.now(),
        'updated_at': timezone.now(),
    }


@pytest.fixture
def indicator_metric_data(indicator_data, metric_data):
    return {
        'indicator_id': Indicators.objects.create(**indicator_data),
        'metric_id': Metrics.objects.create(**metric_data),
        'is_active': True,
        'created_at': timezone.now(),
        'updated_at': timezone.now(),
    }


@pytest.fixture
def score_data(test_data, indicator_metric_data):
    return {
        'score': 90.0,
        'test_id': Tests.objects.create(**test_data),
        'indicator_metric_id': IndicatorMetric.objects.create(
            **indicator_metric_data),
        'is_active': True,
        'created_at': timezone.now(),
        'updated_at': timezone.now(),
    }


@pytest.fixture
def reference_data(indicator_metric_data):
    return {
        'min_score': 70.0,
        'max_score': 100.0,
        'indicator_metric_id': IndicatorMetric.objects.create(
            **indicator_metric_data),
        'is_active': True,
        'created_at': timezone.now(),
        'updated_at': timezone.now(),
    }


@pytest.mark.django_db
def test_create_lab(lab_data):
    """Проверяет создание записи о лаборатории."""
    lab = Labs.objects.create(**lab_data)
    assert lab.name == lab_data['name'], 'Не удалось создать лабораторию'


@pytest.mark.django_db
def test_create_test(test_data):
    """Проверяет создание записи о медицинском тесте."""
    test = Tests.objects.create(**test_data)
    assert test.comment == test_data['comment'], 'Не удалось создать тест'


@pytest.mark.django_db
def test_create_indicator(indicator_data):
    """Проверяет создание записи о показателе медицинского исследования."""
    indicator = Indicators.objects.create(**indicator_data)
    assert indicator.name == indicator_data['name'], (
        'Не удалось создать показатель')


@pytest.mark.django_db
def test_create_metric(metric_data):
    """Проверяет создание записи о метрике (единице измерения)."""
    metric = Metrics.objects.create(**metric_data)
    assert metric.name == metric_data['name'], 'Не удалось создать метрику'


@pytest.mark.django_db
def test_create_indicator_metric(indicator_metric_data):
    """Проверяет создание записи о связи показателя и метрики."""
    indicator_metric = IndicatorMetric.objects.create(**indicator_metric_data)
    assert indicator_metric.indicator_id == indicator_metric_data[
        'indicator_id'], 'Не удалось создать показатель метрики'


@pytest.mark.django_db
def test_create_score(score_data):
    """Проверяет создание записи о количественном значении."""
    score = Scores.objects.create(**score_data)
    assert score.score == score_data['score'], (
        'Не удалось создать количественное значение')


@pytest.mark.django_db
def test_create_reference(reference_data):
    """Проверяет создание записи о справке."""
    reference = Reference.objects.create(**reference_data)
    assert reference.min_score == reference_data['min_score'], (
        'Не удалось создать справку')
