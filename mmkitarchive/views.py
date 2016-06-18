from rest_framework.filters import DjangoFilterBackend

from mmkitcommon.viewsets import MultipleSerializerViewSetMixin, MultipleQuerysetViewSetMixin, NoDeleteViewSet
from mmkitarchive.models import Item, Category
from mmkitarchive import serializers, filters


class ItemViewSet(MultipleSerializerViewSetMixin, MultipleQuerysetViewSetMixin, NoDeleteViewSet):

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

    def perform_create(self, serializer):
        instance = serializer.save()
        user = self.request.user
        instance.log_activity_create(user=user if not user.is_anonymous() else None)

    def perform_update(self, serializer):
        instance = serializer.save()
        user = self.request.user
        instance.log_activity_update(user=user if not user.is_anonymous() else None)


class CategoryViewSet(NoDeleteViewSet):

    queryset = Category.objects.all()
    serializer_class = serializers.CategoryDefaultSerializer
