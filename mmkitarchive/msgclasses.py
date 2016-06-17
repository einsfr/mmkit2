from django.utils.translation import ugettext_lazy as _

MMKITARCHIVE_ITEM_CREATED = 1
MMKITARCHIVE_ITEM_UPDATED = 2

MMKITARCHIVE_CATEGORY_CREATED = 21
MMKITARCHIVE_CATEGORY_UPDATED = 22

msg_classes = {
    MMKITARCHIVE_ITEM_CREATED: ('MMKITARCHIVE_ITEM_CREATED', _('Создан элемент архива')),
    MMKITARCHIVE_ITEM_UPDATED: ('MMKITARCHIVE_ITEM_UPDATED', _('Изменён элемент архива')),

    MMKITARCHIVE_CATEGORY_CREATED: ('MMKITARCHIVE_CATEGORY_CREATED', _('Создана категория элементов архива')),
    MMKITARCHIVE_CATEGORY_UPDATED: ('MMKITARCHIVE_CATEGORY_UPDATED', _('Изменена категория элементов архива')),
}
