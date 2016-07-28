from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User

from . import msgclasses


class MessageClass(models.Model):
    """
    Модель, описывающая класс сообщения в журнале активности
    """

    class Meta:
        verbose_name = _('класс сообщения в журнале активности')
        verbose_name_plural = _('классы сообщений в журнале активности')
        default_permissions = ()

    id = models.PositiveSmallIntegerField(
        primary_key=True,
        editable=False
    )

    name = models.CharField(
        verbose_name=_('название'),
        help_text=_('Название класса сообщения'),
        editable=False,
        max_length=32
    )

    description = models.CharField(
        verbose_name=_('описание'),
        help_text=_('Описание класса сообщения'),
        max_length=255,
        editable=False
    )

    def __str__(self):
        return self.name


class ActivityRecord(models.Model):
    """
    Модель, описывающая сообщение в журнале активности
    """

    class Meta:
        verbose_name = _('запись в журнале активности')
        verbose_name_plural = _('записи в журнале активности')
        default_permissions = ()
        ordering = ('-id', )

    # TODO: в качестве первичного ключа здесь нужно будет использовать BigAutoField, который вроде как будет в 1.10

    dt = models.DateTimeField(
        auto_now=True,
        editable=False,
        db_index=True
    )

    # название имеет значение - если взять другие, то придётся указывать их для GenericForeignKey и GenericRelation
    content_type = models.ForeignKey(
        ContentType,
        related_name='+',
        on_delete=models.CASCADE,
        editable=False
    )

    # название имеет значение - если взять другие, то придётся указывать их для GenericForeignKey и GenericRelation
    object_id = models.BigIntegerField(
        editable=False,
        db_index=True
    )

    content_object = GenericForeignKey()

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='+',
        editable=False,
        null=True
    )

    message_class = models.ForeignKey(
        MessageClass,
        on_delete=models.PROTECT,
        related_name='messages',
        editable=False,
    )

    message = models.TextField(
        blank=True
    )

    def __str__(self):
        return  # TODO

    def get_absolute_url(self) -> str:
        return  # TODO

    @staticmethod
    def get_api_detail_view_name() -> str:
        return 'api:mmkitjournal:activityrecords:detail'  # TODO: надо ещё это реализовать


class ActivityRecordableAbstractModel(models.Model):
    """
    Абстрактная модель для наследования всеми моделями, для которых предполагается ведение записей в журнале активности
    """

    class Meta:
        abstract = True

    activity_records = GenericRelation(
        ActivityRecord,
        related_name='+'
    )

    def log_activity(self, **kwargs) -> None:
        ActivityRecord(content_object=self, **kwargs).save()

    def log_activity_create(self, **kwargs) -> None:
        kwargs['message_class'] = MessageClass.objects.get(pk=msgclasses.MMKIT_OBJECT_CREATED)
        self.log_activity(**kwargs)

    def log_activity_update(self, **kwargs) -> None:
        kwargs['message_class'] = MessageClass.objects.get(pk=msgclasses.MMKIT_OBJECT_UPDATED)
        self.log_activity(**kwargs)
