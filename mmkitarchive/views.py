from rest_framework.filters import DjangoFilterBackend

from mmkitcommon.viewsets import MultipleSerializerViewSetMixin, MultipleQuerysetViewSetMixin
from mmkitjournal.viewsets import ActivityRecordableModelViewSet
from mmkitarchive.models import Item, Category
from mmkitarchive import serializers, filters


class ItemViewSet(MultipleSerializerViewSetMixin, ActivityRecordableModelViewSet):

    queryset = Item.objects.select_related('category').all()
    serializer_class = serializers.ItemDefaultSerializer

    action_serializer_classes = {
        'list': serializers.ItemListSerializer,
        'retrieve': serializers.ItemRetrieveSerializer,
    }

    filter_backends = (DjangoFilterBackend, )
    filter_class = filters.ItemFilter


class CategoryViewSet(MultipleSerializerViewSetMixin, ActivityRecordableModelViewSet):

    queryset = Category.objects.all()
    serializer_class = serializers.CategoryDefaultSerializer

    action_serializer_classes = {
        'retrieve': serializers.CategoryRetrieveSerializer,
    }
