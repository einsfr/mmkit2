from rest_framework import serializers

from mmkitarchive.models import Item, Category


class ItemDefaultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'created', 'author', 'category')


class ItemListSerializer(ItemDefaultSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='api:mmkitarchive:item-detail'
    )

    class Meta(ItemDefaultSerializer.Meta):
        fields = ('url', 'id', 'name', 'created', 'category')
        depth = 1


class ItemRetrieveSerializer(ItemDefaultSerializer):

    class Meta(ItemDefaultSerializer.Meta):
        depth = 1


class CategoryDefaultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', )
