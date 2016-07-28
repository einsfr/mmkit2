from rest_framework import filters
import django_filters

from .models import ActivityRecord


class ActivityRecordFilter(filters.FilterSet):

    dt_min = django_filters.DateFilter(name='dt', lookup_type='gte')
    dt_max = django_filters.DateFilter(name='dt', lookup_type='lte')

    class Meta:
        model = ActivityRecord
        fields = ['dt_min', 'dt_max']
