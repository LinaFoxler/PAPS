from django_filters.rest_framework import FilterSet, UUIDFilter

from api.models import Tests


class TestFilter(FilterSet):
    lab_id = UUIDFilter(field_name='lab_id__id')

    class Meta:
        model = Tests
        fields = ('lab_id',)
