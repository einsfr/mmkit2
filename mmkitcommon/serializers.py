from rest_framework import serializers

from django.contrib.contenttypes.models import ContentType


class ContentTypeDefaultSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContentType
        fields = ('app_label', 'model')
