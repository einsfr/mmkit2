from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins


class NoDeleteViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      GenericViewSet):
    """
    Базовый ViewSet для всех объектов системы, которые не могут быть удалены "просто так"
    """
    pass


# http://stackoverflow.com/questions/22616973/django-rest-framework-use-different-serializers-in-the-same-modelviewset
class MultipleSerializerViewSetMixin:

    def get_serializer_class(self):
        try:
            return self.action_serializer_classes[self.action]
        except (AttributeError, KeyError):
            return super().get_serializer_class()


class MultipleQuerysetViewSetMixin:

    def get_queryset(self):
        try:
            return self.action_querysets[self.action]
        except (AttributeError, KeyError):
            return super().get_queryset()
