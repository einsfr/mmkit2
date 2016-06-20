from rest_framework import serializers

from mmkitarchive.models import Item, Category


class CategoryDefaultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', )


class CategoryListSerializer(CategoryDefaultSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='api:mmkitarchive:category-detail'
    )

    class Meta(CategoryDefaultSerializer.Meta):
        fields = ('url', 'id', 'name')


class ItemDefaultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'created', 'author', 'category')


class ItemListSerializer(ItemDefaultSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='api:mmkitarchive:item-detail'
    )

    category = CategoryDefaultSerializer(
        read_only=True
    )

    class Meta(ItemDefaultSerializer.Meta):
        fields = ('url', 'id', 'name', 'created', 'category')


class ItemRetrieveSerializer(ItemDefaultSerializer):

    category = CategoryDefaultSerializer(
        read_only=True
    )

    class Meta(ItemDefaultSerializer.Meta):
        fields = ('id', 'name', 'description', 'created', 'author', 'category')
