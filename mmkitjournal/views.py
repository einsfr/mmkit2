from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from mmkitjournal.models import ActivityRecord
from mmkitjournal import serializers


class ActivityRecordViewSet(ListModelMixin, GenericViewSet):

    queryset = ActivityRecord.objects.select_related('message_class', 'user', 'content_type').all()
    serializer_class = serializers.ActivityRecordDefaultSerializer
