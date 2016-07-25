import uuid
import os

from django.db import models
from django.contrib.postgres.fields import HStoreField, ArrayField
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from mmkitjournal.models import ActivityRecordableAbstractModel
from mmkitcommon.utils import urlformatter, fs


class StorageObject(models.Model):

    class Meta:
        verbose_name = 'объект в хранилище'
        verbose_name_plural = 'объекты в хранилищах'
        default_permissions = ()
        unique_together = (('storage', 'path'), )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    storage = models.ForeignKey(
        'Storage',
        related_name='stored_objects',
        verbose_name=_('хранилище'),
        help_text=_('Хранилище, в котором размещается объект')
    )

    path = models.CharField(
        max_length=255,
        verbose_name=_('путь к объекту'),
        help_text=_('Путь к объекту относительно корня хранилища (не более 255 символов)')
    )

    def get_url(self, protocol: str) -> urlformatter.UrlFormatResult:
        return self.storage.get_url(self, protocol)

    def get_relative_path(self, inner_path: str = None) -> str:
        if inner_path is None:
            return os.path.normpath(self.path)
        else:
            return os.path.normpath(os.path.join(self.path, inner_path))

    def get_absolute_path(self, inner_path: str = None) -> str:
        return self.storage.get_object_path(self, inner_path)


class Storage(ActivityRecordableAbstractModel):

    class Meta:
        verbose_name = 'хранилище'
        verbose_name_plural = 'хранилища'
        default_permissions = ()

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4
    )

    name = models.CharField(
        verbose_name=_('имя'),
        max_length=255,
        unique=True,
        help_text=_('Имя хранилища (не более 255 символов, должно быть уникальным)')
    )

    base_dir = models.CharField(
        verbose_name=_('корневая директория'),
        max_length=255,
        unique=True,
        help_text=_('Базовая директория хранилища - путь относительно корня всех хранилищ MMKIT_STORAGES_ROOT_DIR '
                    '(не более 255 символов, должен быть уникальным)')
    )

    access_protocols = HStoreField(
        verbose_name=_('Протоколы доступа'),
        blank=True,
        default={},
        help_text=_('Словарь, содержащий пары вида <протокол_доступа>: <базовая часть URL для доступа> '
                    '(по-умолчанию - пустой)')
    )

    read_only = models.BooleanField(
        verbose_name=_('только для чтения'),
        default=True,
        help_text=_('Если True - хранилище можно использовать только для чтения (по-умолчанию - True)')
    )

    allowed_usage = ArrayField(
        models.CharField(max_length=32),
        verbose_name=_('Разрешённые варианты использования'),
        blank=True,
        default=[],
        help_text=_('Массив разрешённых вариантов использования хранилища (по-умолчанию - пустой)')
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self) -> str:
        return  # TODO

    @staticmethod
    def get_api_detail_view_name() -> str:
        return  # TODO

    def get_url(self, obj: StorageObject, protocol: str) -> urlformatter.UrlFormatResult:
        try:
            base_url = self.access_protocols[protocol]
        except KeyError:
            return None
        return urlformatter.format_url('{}/{}'.format(base_url, obj.path)),

    def get_base_path(self) -> str:
        return os.path.normpath(os.path.join(
            settings.MMKIT_STORAGES_ROOT_DIR,
            self.base_dir
        ))

    def get_object_path(self, obj: StorageObject, inner_path: str = None) -> str:
        if inner_path is None:
            return os.path.normpath(os.path.join(
                self.get_base_path(),
                obj.path
            ))
        else:
            return os.path.normpath(os.path.join(
                self.get_base_path(),
                obj.path
            ))

    def get_or_create_object(self, path: str) -> StorageObject:
        try:
            obj = self.stored_objects.get(path__iexact=path)
        except StorageObject.DoesNotExist:
            obj = StorageObject(path=path, storage=self).save()
        return obj
