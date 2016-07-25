import uuid
import os
from urllib import parse
import shutil

from django.db import models
from django.contrib.postgres.fields import HStoreField, ArrayField
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from mmkitjournal.models import ActivityRecordableAbstractModel
from mmkitcommon.utils import fs as fs_utils
from . import exceptions as storage_exceptions


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

    def get_url(self, protocol: str) -> str:
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

    INIT_MODE_SKIP_IF_EXISTS = 0
    INIT_MODE_REWRITE_IF_EXISTS = 1

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

    def get_url(self, obj: StorageObject, protocol: str) -> str:
        try:
            base_url = self.access_protocols[protocol]
        except KeyError:
            return None
        return parse.urljoin(base_url, obj.path, allow_fragments=False)

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

    def contains(self, path: str, check_existence: bool = True) -> bool:
        base_path = self.get_base_path()
        full_path = os.path.normpath(os.path.join(base_path, path))
        return fs_utils.in_path(base_path, full_path) and (not check_existence or os.path.exists(full_path))

    @classmethod
    def init_storage_root(cls, init_mode: int = INIT_MODE_SKIP_IF_EXISTS) -> None:
        storages_root = os.path.normpath(settings.MMKIT_STORAGES_ROOT_DIR)
        if not os.path.exists(storages_root):
            os.makedirs(storages_root, settings.MMKIT_STORAGES_ROOT_MODE)
        else:
            if init_mode == cls.INIT_MODE_SKIP_IF_EXISTS:
                pass  # TODO: добавить запись в лог с уведомлением
            elif init_mode == cls.INIT_MODE_REWRITE_IF_EXISTS:
                if settings.MMKIT_STORAGES_FORBID_ROOT_REWRITE:
                    raise RuntimeError(storage_exceptions.STORAGES_ROOT_REWRITE_FORBIDDEN)
                else:
                    # Предварительное переименования появилось из-за того, что в Windows существует задержка между
                    # исполнением команды rmtree и фактическим удалением папки, а переименование происходит сразу
                    tmp_name = '_{}'.format(storages_root)
                    os.rename(storages_root, tmp_name)
                    shutil.rmtree(tmp_name)
                    os.mkdir(storages_root, settings.MMKIT_STORAGES_ROOT_MODE)
            else:
                raise ValueError(storage_exceptions.STORAGES_INIT_MODE_UNKNOWN)

    def init_storage_base(self, init_mode: int = INIT_MODE_SKIP_IF_EXISTS) -> None:
        storages_root = os.path.normpath(settings.MMKIT_STORAGES_ROOT_DIR)
        if not os.path.exists(storages_root):
            raise RuntimeError(storage_exceptions.STORAGES_ROOT_NOT_FOUND % {'root_dir': storages_root})
        base_path = self.get_base_path()
        if not os.path.exists(base_path):
            os.mkdir(base_path, settings.MMKIT_STORAGES_BASE_MODE)
        else:
            if init_mode == self.INIT_MODE_SKIP_IF_EXISTS:
                pass  # TODO: добавить запись в лог с уведомлением
            elif init_mode == self.INIT_MODE_REWRITE_IF_EXISTS:
                if settings.MMKIT_STORAGES_FORBID_BASE_REWRITE:
                    raise RuntimeError(storage_exceptions.STORAGES_BASE_REWRITE_FORBIDDEN)
                else:
                    tmp_name = '_{}'.format(base_path)
                    os.rename(base_path, tmp_name)
                    shutil.rmtree(tmp_name)
                    os.mkdir(base_path, settings.MMKIT_STORAGES_BASE_MODE)
            else:
                raise ValueError(storage_exceptions.STORAGES_INIT_MODE_UNKNOWN)
