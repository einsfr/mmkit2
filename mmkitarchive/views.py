from rest_framework import generics

from mmkitarchive import models, serializers


class ItemList(generics.ListCreateAPIView):
    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer
