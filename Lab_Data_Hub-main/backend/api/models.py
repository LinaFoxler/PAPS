import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from api.constants import DECIMAL_PLACES, MAX_DIGITS, MAX_LENGTH

User = get_user_model()


class Labs(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=MAX_LENGTH)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField()

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'Лаборатория'
        verbose_name_plural = 'Лаборатории'

    def __str__(self):
        return self.name


class Tests(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField()
    comment = models.CharField(
        max_length=MAX_LENGTH,
        null=True
    )
    lab_id = models.ForeignKey(
        Labs,
        on_delete=models.CASCADE,
        related_name='tests'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField()

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return f'Test ID: {self.id}'


class Indicators(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=MAX_LENGTH)
    description = models.CharField(
        max_length=MAX_LENGTH,
        null=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField()

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'Показатель'
        verbose_name_plural = 'Показатели'

    def __str__(self):
        return self.name


class Metrics(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=MAX_LENGTH)
    description = models.CharField(
        max_length=MAX_LENGTH,
        null=True
    )
    unit = models.CharField(max_length=MAX_LENGTH)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField()

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'Метрика'
        verbose_name_plural = 'Метрики'

    def __str__(self):
        return self.name


class IndicatorMetric(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    indicator_id = models.ForeignKey(
        Indicators,
        on_delete=models.CASCADE,
        related_name='indicator_metrics'
    )
    metric_id = models.ForeignKey(
        Metrics,
        on_delete=models.CASCADE,
        related_name='indicator_metrics'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField()

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'Показатель метрики'
        verbose_name_plural = 'Показатели метрики'

    def __str__(self):
        return f'IndicatorMetric ID: {self.id}'


class Scores(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    score = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES
    )
    test_id = models.ForeignKey(
        Tests,
        on_delete=models.CASCADE,
        related_name='scores'
    )
    indicator_metric_id = models.ForeignKey(
        IndicatorMetric,
        on_delete=models.CASCADE,
        related_name='scores'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField()

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'Количественное значение'
        verbose_name_plural = 'Количественное значение'

    def __str__(self):
        return f'Score ID: {self.id}'


class Reference(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    min_score = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES
    )
    max_score = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES
    )
    indicator_metric_id = models.ForeignKey(
        IndicatorMetric,
        on_delete=models.CASCADE,
        related_name='references'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField()

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'Справка'
        verbose_name_plural = 'Справки'

    def __str__(self):
        return f'Reference ID: {self.id}'
