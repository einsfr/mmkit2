from rest_framework.filters import DjangoFilterBackend
from rest_framework.decorators import detail_route
from rest_framework.response import Response

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

    @detail_route(methods=['GET'])
    def links(self, request, pk=None):
        item = Item.objects.get(pk=pk)
        linked_items = item.linked.all()
        page = self.paginate_queryset(linked_items)
        if page is not None:
            serializer = serializers.ItemLinkSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        else:
            serializer = serializers.ItemLinkSerializer(linked_items, many=True, context={'request': request})
            return Response(serializer.data)


class CategoryViewSet(MultipleSerializerViewSetMixin, ActivityRecordableModelViewSet):

    queryset = Category.objects.all()
    serializer_class = serializers.CategoryDefaultSerializer

    action_serializer_classes = {
        'retrieve': serializers.CategoryRetrieveSerializer,
    }
