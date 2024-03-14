from rest_framework import serializers

from api.models import (IndicatorMetric, Indicators, Labs, Metrics, Reference,
                        Scores, Tests, User)


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        ref_name = 'ApiUser'

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')
        ref_name = 'DjoserUser'


class LabsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Labs
        fields = '__all__'


class IndicatorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Indicators
        fields = '__all__'


class MetricsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Metrics
        fields = '__all__'


class ScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Scores
        fields = '__all__'


class ReferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reference
        fields = '__all__'


class IndicatorMetricSerializer(serializers.ModelSerializer):

    class Meta:
        model = IndicatorMetric
        fields = '__all__'


class TestSerializer(serializers.ModelSerializer):
    duration_seconds = serializers.SerializerMethodField()
    results = serializers.SerializerMethodField()

    class Meta:
        model = Tests
        fields = ('id', 'lab_id', 'duration_seconds', 'results')

    def get_results(self, obj):
        results = []

        for score in obj.scores.all():
            reference = score.indicator_metric_id.references.first()
            is_within_normal_range = None

            if reference:
                min_score = reference.min_score
                max_score = reference.max_score
                current_score = score.score
                is_within_normal_range = (
                    min_score <= current_score <= max_score)

            result = {
                'id': score.id,
                'score': score.score,
                'indicator_name': score.indicator_metric_id.indicator_id.name,
                'metric_name': score.indicator_metric_id.metric_id.name,
                'metric_unit': score.indicator_metric_id.metric_id.unit,
                'is_within_normal_range': is_within_normal_range
            }
            results.append(result)

        return results

    def get_duration_seconds(self, obj):
        if obj.started_at and obj.completed_at:
            duration = (obj.completed_at - obj.started_at).total_seconds()
            return int(duration)
        return None


class TestCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tests
        fields = '__all__'
