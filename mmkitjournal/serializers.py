from rest_framework import serializers

from mmkitjournal.models import ActivityRecord
from mmkitcommon.serializers import ContentTypeDefaultSerializer


class ActivityRecordListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivityRecord
        fields = ('id', 'dt', 'content_type', 'object_id', 'user', 'message_class', 'message')

    content_type = ContentTypeDefaultSerializer(read_only=True)

    user = serializers.StringRelatedField()  # TODO: проверить, как это будет вести себя с user = None

    message_class = serializers.StringRelatedField()
