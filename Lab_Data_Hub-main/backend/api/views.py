from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.filters import TestFilter
from api.models import (IndicatorMetric, Indicators, Labs, Metrics, Reference,
                        Scores, Tests)
from api.serializers import (IndicatorMetricSerializer, IndicatorsSerializer,
                             LabsSerializer, MetricsSerializer,
                             ReferenceSerializer, ScoreSerializer,
                             TestCreateSerializer, TestSerializer)


class LabsViewSet(ModelViewSet):
    queryset = Labs.objects.all()
    serializer_class = LabsSerializer


class IndicatorsViewSet(ModelViewSet):
    queryset = Indicators.objects.all()
    serializer_class = IndicatorsSerializer


class MetricsViewSet(ModelViewSet):
    queryset = Metrics.objects.all()
    serializer_class = MetricsSerializer


class IndicatorMetricViewSet(ModelViewSet):
    queryset = IndicatorMetric.objects.all()
    serializer_class = IndicatorMetricSerializer


class ScoresViewSet(ModelViewSet):
    queryset = Scores.objects.all()
    serializer_class = ScoreSerializer


class ReferenceViewSet(ModelViewSet):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer


class TestsViewSet(ModelViewSet):
    queryset = Tests.objects.all()
    serializer_class = TestCreateSerializer


class TestResultViewSet(ModelViewSet):
    queryset = Tests.objects.all()
    serializer_class = TestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TestFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['test_id'] = self.kwargs.get('pk')
        return context

    def get_object(self):
        test_id = self.kwargs.get('pk')
        try:
            return Tests.objects.get(id=test_id)
        except Tests.DoesNotExist:
            return None

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed('POST')
