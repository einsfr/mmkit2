from rest_framework import serializers

from mmkitarchive.models import Item, Category

# Category


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('url', 'id', 'name')

    url = serializers.HyperlinkedIdentityField(
        view_name=Category.get_api_detail_view_name()
    )


class CategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', )


class CategoryRetrieveUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')

# Item


class ItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('name', 'description', 'created', 'author', 'category')


class ItemListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('url', 'id', 'name', 'created', 'category')

    url = serializers.HyperlinkedIdentityField(
        view_name=Item.get_api_detail_view_name()
    )

    category = CategoryListSerializer(
        read_only=True
    )


class ItemUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'created', 'author', 'category')


class ItemRetrieveSerializer(ItemUpdateSerializer):

    class Meta(ItemUpdateSerializer.Meta):
        pass

    category = CategoryListSerializer(
        read_only=True
    )
