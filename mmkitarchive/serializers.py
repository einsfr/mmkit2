from rest_framework import serializers

from mmkitarchive.models import Item


class ItemDefaultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('name', 'description', 'created', 'author', 'category')


class ItemListSerializer(ItemDefaultSerializer):

    class Meta(ItemDefaultSerializer.Meta):
        depth = 1
