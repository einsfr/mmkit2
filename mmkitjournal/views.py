from rest_framework import generics

from mmkitjournal.models import ActivityRecord
from mmkitjournal import serializers


class ActivityRecordView(generics.ListAPIView):

    queryset = ActivityRecord.objects.select_related('message_class', 'user', 'content_type').all()
    serializer_class = serializers.ActivityRecordListSerializer
