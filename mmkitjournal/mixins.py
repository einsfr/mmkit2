from django.db import transaction
from rest_framework.serializers import BaseSerializer

from .models import ActivityRecordableAbstractModel


class CreateARModelMixin:

    def perform_create(self, serializer: BaseSerializer) -> None:
        with transaction.atomic():
            instance = serializer.save()
            user = self.request.user  # Из-за этой строки можно использовать только с наследниками APIView
            instance.log_activity_create(user=user if not user.is_anonymous() else None)
            self.hook_post_create(instance)

    def hook_post_create(self, instance: ActivityRecordableAbstractModel) -> None:
        pass


class UpdateARModelMixin:

    def perform_update(self, serializer: BaseSerializer) -> None:
        with transaction.atomic():
            instance = serializer.save()
            user = self.request.user  # Из-за этой строки можно использовать только с наследниками APIView
            instance.log_activity_update(user=user if not user.is_anonymous() else None)
            self.hook_post_update(instance)

    def hook_post_update(self, instance: ActivityRecordableAbstractModel) -> None:
        pass
