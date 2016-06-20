from django.utils.translation import ugettext_lazy as _

MMKIT_OBJECT_CREATED = 1
MMKIT_OBJECT_UPDATED = 2

msg_classes = {
    MMKIT_OBJECT_CREATED: ('MMKIT_OBJECT_CREATED', _('Создан объект')),
    MMKIT_OBJECT_UPDATED: ('MMKIT_OBJECT_UPDATED', _('Изменён объект')),
}
