from rest_framework.filters import DjangoFilterBackend
from rest_framework import generics, mixins
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from mmkitcommon.viewsets import MultipleSerializerViewSetMixin, MultipleQuerysetViewSetMixin
from mmkitjournal.viewsets import ActivityRecordableModelViewSet
from mmkitarchive.models import Item, Category
from mmkitarchive import serializers, filters


@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='API')
    return response.Response(generator.get_schema(request=request))


class ItemListView(mixins.ListModelMixin, generics.GenericAPIView):

    queryset = Item.objects.select_related('category').all()
    serializer_class = serializers.ItemListSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = filters.ItemFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, args, kwargs)


class ItemCreateView(mixins.CreateModelMixin, generics.GenericAPIView):

    serializer_class = serializers.ItemCreateSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ItemViewSet(MultipleSerializerViewSetMixin, ActivityRecordableModelViewSet):

    queryset = Item.objects.select_related('category').all()

    action_serializer_classes = {
        'list': serializers.ItemListSerializer,
        # 'retrieve': serializers.ItemRetrieveSerializer,
    }

    filter_backends = (DjangoFilterBackend, )
    filter_class = filters.ItemFilter


class CategoryViewSet(MultipleSerializerViewSetMixin, ActivityRecordableModelViewSet):

    queryset = Category.objects.all()
    serializer_class = serializers.CategoryDefaultSerializer

    action_serializer_classes = {
        'retrieve': serializers.CategoryRetrieveSerializer,
    }
