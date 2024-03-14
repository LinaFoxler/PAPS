from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from api.views import (IndicatorMetricViewSet, IndicatorsViewSet, LabsViewSet,
                       MetricsViewSet, ReferenceViewSet, ScoresViewSet,
                       TestResultViewSet, TestsViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Lab_data_project API",
        default_version='v1',
        description="Lab_data_project",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register('labs', LabsViewSet, basename='labs')
v1_router.register('tests', TestsViewSet, basename='tests')
v1_router.register('indicators', IndicatorsViewSet, basename='indicators')
v1_router.register('metrics', MetricsViewSet, basename='metrics')
v1_router.register('indicator-metrics', IndicatorMetricViewSet,
                   basename='indicator-metrics')
v1_router.register('scores', ScoresViewSet, basename='scores')
v1_router.register('references', ReferenceViewSet, basename='references')
v1_router.register('test-results', TestResultViewSet,
                   basename='test-results')


urlpatterns = [
    path('', include(v1_router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
