from rest_framework import viewsets

from mmkitcommon.viewsets import MultipleSerializerViewSetMixin
from mmkitarchive.models import Item
from mmkitarchive.serializers import ItemDefaultSerializer, ItemListSerializer


class ItemViewSet(MultipleSerializerViewSetMixin, viewsets.ModelViewSet):

    queryset = Item.objects.all()
    serializer_class = ItemDefaultSerializer

    action_serializer_classes = {
        'list': ItemListSerializer,
    }
