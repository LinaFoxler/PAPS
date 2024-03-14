from django.contrib import admin

from api.models import (IndicatorMetric, Indicators, Labs, Metrics, Reference,
                        Scores, Tests)


@admin.register(Labs)
class LabsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active',
                    'created_at', 'updated_at',)


@admin.register(Tests)
class TestsAdmin(admin.ModelAdmin):
    list_display = ('id', 'started_at', 'completed_at', 'comment',
                    'lab_id', 'is_active', 'created_at', 'updated_at')


@admin.register(Indicators)
class IndicatorsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description',
                    'is_active', 'created_at', 'updated_at')


@admin.register(Metrics)
class MetricsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'unit',
                    'is_active', 'created_at', 'updated_at')


@admin.register(IndicatorMetric)
class IndicatorMetricAdmin(admin.ModelAdmin):
    list_display = ('id', 'indicator_id', 'metric_id',
                    'is_active', 'created_at', 'updated_at')


@admin.register(Scores)
class ScoresAdmin(admin.ModelAdmin):
    list_display = ('id', 'score', 'test_id', 'indicator_metric_id',
                    'is_active', 'created_at', 'updated_at')


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'min_score', 'max_score',
                    'indicator_metric_id', 'is_active', 'created_at',
                    'updated_at')
