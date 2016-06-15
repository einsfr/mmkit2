from rest_framework import viewsets
from rest_framework.filters import DjangoFilterBackend

from mmkitcommon.viewsets import MultipleSerializerViewSetMixin, MultipleQuerysetViewSetMixin
from mmkitarchive.models import Item, Category
from mmkitarchive import serializers, filters


class ItemViewSet(MultipleSerializerViewSetMixin, MultipleQuerysetViewSetMixin, viewsets.ModelViewSet):

    queryset = Item.objects.all()
    serializer_class = serializers.ItemDefaultSerializer

    action_serializer_classes = {
        'list': serializers.ItemListSerializer,
        'retrieve': serializers.ItemRetrieveSerializer,
    }

    action_querysets = {
        'list': Item.objects.all().select_related('category'),
        'retrieve': Item.objects.all().select_related('category'),
    }

    filter_backends = (DjangoFilterBackend, )
    filter_class = filters.ItemFilter


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = serializers.CategoryDefaultSerializer
