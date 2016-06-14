from rest_framework import serializers

from mmkitarchive import models


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = ('name', )


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Item
        fields = ('name', 'description', 'created', 'author', 'category')
