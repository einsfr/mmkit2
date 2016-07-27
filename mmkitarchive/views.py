from rest_framework.filters import DjangoFilterBackend, OrderingFilter
from rest_framework import generics

from mmkitarchive.models import Item, Category
from mmkitarchive import serializers, filters
from mmkitjournal import mixins as journal_mixins


class ItemListCreateView(journal_mixins.CreateARModelMixin, generics.ListCreateAPIView):

    queryset = Item.objects.select_related('category').all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = filters.ItemFilter
    ordering_fields = ('id', 'name', 'created')

    def get_serializer_class(self):
        if self.request.method == 'GET':  # list
            return serializers.ItemListSerializer
        elif self.request.method == 'POST':  # create
            return serializers.ItemCreateSerializer


class ItemRetrieveUpdateView(journal_mixins.UpdateARModelMixin, generics.RetrieveUpdateAPIView):

    queryset = Item.objects.select_related('category').all()

    def get_serializer_class(self):
        if self.request.method == 'GET':  # retrieve
            return serializers.ItemRetrieveSerializer
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':  # update
            return serializers.ItemUpdateSerializer


class CategoryListCreateView(journal_mixins.CreateARModelMixin, generics.ListCreateAPIView):

    queryset = Category.objects.all()
    filter_backends = (OrderingFilter, )
    ordering_fields = ('id', 'name')

    def get_serializer_class(self):
        if self.request.method == 'GET':  # list
            return serializers.CategoryListSerializer
        elif self.request.method == 'POST':  # create
            return serializers.CategoryCreateSerializer


class CategoryRetrieveUpdateView(journal_mixins.UpdateARModelMixin, generics.RetrieveUpdateAPIView):

    queryset = Category.objects.all()
    serializer_class = serializers.CategoryRetrieveUpdateSerializer

