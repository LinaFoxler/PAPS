import pytest
from django.utils import timezone

from api.models import (IndicatorMetric, Indicators, Labs, Metrics, Reference,
                        Scores, Tests, User)
from api.serializers import (IndicatorMetricSerializer, IndicatorsSerializer,
                             LabsSerializer, MetricsSerializer,
                             ReferenceSerializer, ScoreSerializer,
                             TestCreateSerializer, TestSerializer,
                             UserCreateSerializer, UserSerializer)


@pytest.fixture
def lab_data():
    return {
        'name': 'Лаборатория 1',
        'is_active': True,
        'created_at': timezone.now(),
        'updated_at': timezone.now(),
    }


@pytest.fixture
def indicators_data():
    return {
        'name': 'Показатель 1',
        'description': 'Описание 1',
        'is_active': True,
        'created_at': timezone.now(),
        'updated_at': timezone.now(),
    }


@pytest.fixture
def metrics_data():
    return {
        'name': 'Метрика 1',
        'description': 'Описание 1',
        'unit': 'Единица измерения 1',
        'is_active': True,
        'created_at': timezone.now(),
        'updated_at': timezone.now(),
    }


@pytest.fixture
def scores_data(indicators_data, metrics_data, test_data):
    indicator_metric = IndicatorMetric.objects.create(
        indicator_id=Indicators.objects.create(**indicators_data),
        metric_id=Metrics.objects.create(**metrics_data),
        is_active=True,
        created_at=timezone.now(),
        updated_at=timezone.now()
    )
    test = Tests.objects.create(**test_data)
    test_id = test.id
    return {
        'score': 90.0,
        'indicator_metric_id': indicator_metric,
        'test_id': test_id,
        'is_active': True,
        'created_at': timezone.now(),
        'updated_at': timezone.now(),
    }


@pytest.fixture
def reference_data(indicators_data, metrics_data, indicator_metric_data):
    indicator_metric = IndicatorMetric.objects.create(**indicator_metric_data)
    return {
        'min_score': 70,
        'max_score': 100,
        'indicator_metric_id': indicator_metric,
        'is_active': True,
        'created_at': timezone.now(),
        'updated_at': timezone.now(),
    }


@pytest.fixture
def indicator_metric_data(indicators_data, metrics_data):
    return {
        'indicator_id': Indicators.objects.create(**indicators_data),
        'metric_id': Metrics.objects.create(**metrics_data),
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


@pytest.mark.django_db
def test_user_create_serializer():
    """Проверяет, что сериализатор UserCreateSerializer проходит валидацию
    при передаче корректных данных."""
    data = {
        'email': 'test@example.com',
        'username': 'testuser',
        'password': 'testpassword',
    }
    serializer = UserCreateSerializer(data=data)
    assert serializer.is_valid(
    ), (f'Сериализатор UserCreateSerializer не прошел валидацию.'
        f' Ошибки: {serializer.errors}')


@pytest.mark.django_db
def test_user_serializer():
    """Проверяет, что сериализатор UserSerializer возвращает
    правильное имя пользователя."""
    user = User.objects.create(username='testuser', email='test@example.com')
    serializer = UserSerializer(instance=user)
    expected_username = 'testuser'
    assert serializer.data[
        'username'] == expected_username, (
            f'Сериализатор UserSerializer'
            f' вернул неверное имя пользователя.'
            f' Ожидаем: {expected_username},'
            f' Получено: {serializer.data["username"]}'
    )


@pytest.mark.django_db
def test_labs_serializer(lab_data):
    """Проверяет, что сериализатор LabsSerializer возвращает
    правильное имя лаборатории."""
    lab = Labs.objects.create(**lab_data)
    serializer = LabsSerializer(instance=lab)
    assert serializer.data['name'] == lab_data[
        'name'], (f'Сериализатор LabsSerializer вернул неверное имя'
                  f' лаборатории. Ожидаем: {lab_data["name"]},'
                  f' Получено: {serializer.data["name"]}')


@pytest.mark.django_db
def test_indicators_serializer(indicators_data):
    """Проверяет, что сериализатор IndicatorsSerializer возвращает
    правильное имя показателя."""
    indicator = Indicators.objects.create(**indicators_data)
    serializer = IndicatorsSerializer(instance=indicator)
    assert serializer.data['name'] == indicators_data[
        'name'], (f'Сериализатор IndicatorsSerializer вернул неверное имя'
                  f' показателя. Ожидаем: {indicators_data["name"]},'
                  f' Получено: {serializer.data["name"]}')


@pytest.mark.django_db
def test_metrics_serializer(metrics_data):
    """Проверяет, что сериализатор MetricsSerializer возвращает
    правильное имя метрики."""
    metric = Metrics.objects.create(**metrics_data)
    serializer = MetricsSerializer(instance=metric)
    assert serializer.data['name'] == metrics_data[
        'name'], (f'Сериализатор MetricsSerializer вернул неверное'
                  f' имя метрики. Ожидаем: {metrics_data["name"]},'
                  f' Получено: {serializer.data["name"]}')


@pytest.mark.django_db
def test_score_serializer(scores_data, test_data):
    """Проверяет, что сериализатор ScoreSerializer возвращает
    правильное количество баллов."""
    test = Tests.objects.create(**test_data)
    scores_data['test_id'] = test
    score = Scores.objects.create(**scores_data)
    serializer = ScoreSerializer(instance=score)
    expected_score = f'{scores_data["score"]:.2f}'

    assert serializer.data[
        'score'] == expected_score, (f'Сериализатор ScoreSerializer вернул'
                                     f' неверное количество баллов.'
                                     f' Ожидаем: {expected_score},'
                                     f' Получено: {serializer.data["score"]}')


@pytest.mark.django_db
def test_reference_serializer(reference_data, indicator_metric_data):
    """Проверяет, что сериализатор ReferenceSerializer возвращает
    правильное минимальное значение справки."""
    indicator_metric = IndicatorMetric.objects.create(**indicator_metric_data)
    reference_data['indicator_metric_id'] = indicator_metric
    reference = Reference.objects.create(**reference_data)
    serializer = ReferenceSerializer(instance=reference)
    expected_min_score = f'{reference_data["min_score"]:.2f}'
    assert serializer.data[
        'min_score'] == expected_min_score, (
            f'Сериализатор ReferenceSerializer вернул'
            f' неверное минимальное значение. Ожидаем: {expected_min_score},'
            f' Получено: {serializer.data["min_score"]}')


@pytest.mark.django_db
def test_indicator_metric_serializer(indicator_metric_data):
    """Проверяет, что сериализатор IndicatorMetricSerializer возвращает
    правильный идентификатор показателя."""
    indicator_metric = IndicatorMetric.objects.create(**indicator_metric_data)
    serializer = IndicatorMetricSerializer(instance=indicator_metric)
    assert serializer.data['indicator_id'] == indicator_metric_data[
        'indicator_id'].id, (
            f'Сериализатор IndicatorMetricSerializer вернул'
            f' неверный идентификатор показателя.'
            f' Ожидаем: {indicator_metric_data["indicator_id"].id},'
            f' Получено: {serializer.data["indicator_id"]}')


@pytest.mark.django_db
def test_test_serializer(test_data):
    """Проверяет, что сериализатор TestSerializer возвращает
    правильный комментарий к тесту."""
    test_data['comment'] = None
    test = Tests.objects.create(**test_data)
    serializer = TestSerializer(instance=test)
    assert serializer.data.get('comment') == test_data.get(
        'comment'), (
            f'Сериализатор TestSerializer вернул неверный комментарий к тесту.'
            f' Ожидаем: {test_data.get("comment")},'
            f' Получено: {serializer.data.get("comment")}')


@pytest.fixture
def test_create_serializer(lab_data):
    test_data = {
        'started_at': timezone.now(),
        'completed_at': timezone.now(),
        'comment': 'Комментарий к тесту',
        'is_active': True,
        'created_at': timezone.now(),
        'updated_at': timezone.now(),
    }
    return test_data


def test_test_create_serializer(test_create_serializer):
    """Проверяет, что сериализатор TestCreateSerializer вызывает
    ошибку валидации для недопустимых данных."""
    serializer = TestCreateSerializer(data=test_create_serializer)
    assert not serializer.is_valid(
    ), ('Сериализатор TestCreateSerializer должен вызывать ошибку валидации'
        ' для недопустимых данных')
