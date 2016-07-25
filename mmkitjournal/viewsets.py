from django.db import transaction

from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import BaseSerializer

from .models import ActivityRecordableAbstractModel


class ActivityRecordableModelViewSet(ModelViewSet):

    def perform_create(self, serializer: BaseSerializer) -> None:
        with transaction.atomic():
            instance = serializer.save()
            user = self.request.user
            instance.log_activity_create(user=user if not user.is_anonymous() else None)
            self.hook_post_create(instance)

    def hook_post_create(self, instance: ActivityRecordableAbstractModel) -> None:
        pass

    def perform_update(self, serializer: BaseSerializer) -> None:
        with transaction.atomic():
            instance = serializer.save()
            user = self.request.user
            instance.log_activity_update(user=user if not user.is_anonymous() else None)
            self.hook_post_update(instance)

    def hook_post_update(self, instance: ActivityRecordableAbstractModel) -> None:
        pass
