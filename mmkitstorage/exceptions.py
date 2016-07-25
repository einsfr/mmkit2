from django.utils.translation import ugettext_lazy as _

STORAGES_ROOT_REWRITE_FORBIDDEN = _('Корневая директория хранилищ не может быть изменена '
                                    '(см. параметр конфигурации MMKIT_STORAGES_FORBID_ROOT_REWRITE).')
STORAGES_BASE_REWRITE_FORBIDDEN = _('Базовая папка хранилища не может быть изменена '
                                    '(см. параметр конфигурации MMKIT_STORAGES_FORBID_BASE_REWRITE).')
STORAGES_INIT_MODE_UNKNOWN = _('Неизвестное значение режима инициализации хранилища.')
STORAGES_ROOT_NOT_FOUND = _('Корневая директория хранилищ "%(root_dir)s" не существует.')
