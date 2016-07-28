from rest_framework import generics
from rest_framework.filters import DjangoFilterBackend

from mmkitjournal.models import ActivityRecord
from mmkitjournal import serializers
from . import filters


class ActivityRecordView(generics.ListAPIView):

    queryset = ActivityRecord.objects.select_related('message_class', 'user', 'content_type').all()
    serializer_class = serializers.ActivityRecordListSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = filters.ActivityRecordFilter
