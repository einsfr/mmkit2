from rest_framework import filters
import django_filters

from mmkitarchive.models import Item


class ItemFilter(filters.FilterSet):

    created_min = django_filters.DateFilter(name='created', lookup_type='gte')
    created_max = django_filters.DateFilter(name='created', lookup_type='lte')

    class Meta:
        model = Item
        fields = ['category', 'created_min', 'created_max', 'linked']
