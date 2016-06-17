from rest_framework import serializers

from mmkitjournal.models import ActivityRecord


class ActivityRecordDefaultSerializer(serializers.ModelSerializer):

    content_type = serializers.StringRelatedField()

    user = serializers.StringRelatedField()  # TODO: проверить, как это будет вести себя с user = None

    message_class = serializers.StringRelatedField()

    class Meta:
        model = ActivityRecord
        fields = ('id', 'dt', 'content_type', 'object_id', 'user', 'message_class', 'message')
