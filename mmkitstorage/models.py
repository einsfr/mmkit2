import uuid

from django.db import models
from django.contrib.postgres.fields import HStoreField, ArrayField
from django.utils.translation import ugettext_lazy as _

from mmkitjournal.models import ActivityRecordableAbstractModel


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

    def get_absolute_url(self):
        return  # TODO

    @staticmethod
    def get_api_detail_view_name():
        return  # TODO


