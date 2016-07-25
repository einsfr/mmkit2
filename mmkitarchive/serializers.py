from rest_framework import serializers

from mmkitarchive.models import Item, Category


class CategoryDefaultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'url')

    url = serializers.HyperlinkedIdentityField(
        view_name=Category.get_api_detail_view_name()
    )


class CategoryRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')


class ItemDefaultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'created', 'author', 'category')


class ItemListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('url', 'id', 'name', 'created', 'category')

    url = serializers.HyperlinkedIdentityField(
        view_name=Item.get_api_detail_view_name()
    )

    category = CategoryDefaultSerializer(
        read_only=True
    )


class ItemLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('url', 'id', 'name')

    url = serializers.HyperlinkedIdentityField(
        view_name=Item.get_api_detail_view_name()
    )


class ItemRetrieveSerializer(ItemDefaultSerializer):

    class Meta(ItemDefaultSerializer.Meta):
        pass

    category = CategoryDefaultSerializer(
        read_only=True
    )
