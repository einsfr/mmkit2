from django.db import models
from django.utils.translation import ugettext_lazy as _

from mmkitjournal.models import ActivityRecordableAbstractModel


class Category(ActivityRecordableAbstractModel):
    """
    Модель, описывающая категорию элемента архива
    """

    class Meta:
        verbose_name = _('категория элемента архива')
        verbose_name_plural = _('категории элементов архива')
        default_permissions = ()

    name = models.CharField(
        verbose_name=_('название'),
        help_text=_('Название категории (не более 64 символов, должно быть уникальным)'),
        max_length=64,
        unique=True,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self) -> str:
        return  # TODO

    @staticmethod
    def get_api_detail_view_name() -> str:
        return 'api:mmkitarchive:categories:detail'


class Item(ActivityRecordableAbstractModel):
    """
    Модель, описывающая элемент архива
    """

    class Meta:
        verbose_name = _('элемент архива')
        verbose_name_plural = _('элементы архива')
        default_permissions = ()

    name = models.CharField(
        verbose_name=_('название'),
        help_text=_('Название элемента (не более 255 символов, должно быть уникальным)'),
        max_length=255,
        unique=True,
    )

    description = models.TextField(
        verbose_name=_('описание'),
        help_text=_('Развёрнутое описание элемента (необязательно)'),
        blank=True,
    )

    created = models.DateField(
        verbose_name=_('дата создания'),
        help_text=_('Дата создания элемента (необязательно)'),
        null=True,
        db_index=True
    )

    author = models.CharField(
        verbose_name=_('автор'),
        help_text=_('Автор(ы) элемента'),
        max_length=255,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='items',
        verbose_name=_('категория'),
    )

    linked = models.ManyToManyField(
        "self",
        verbose_name=_('связанные элементы')
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self) -> str:
        return  # TODO

    @staticmethod
    def get_api_detail_view_name() -> str:
        return 'api:mmkitarchive:items:detail'
