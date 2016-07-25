import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from mmkitstorage.models import Storage
from mmkitstorage import exceptions as storage_exceptions
from mmkitcommon.utils import fs as fs_utils


class Command(BaseCommand):

    help = _('Создаёт новое хранилище.')

    def add_arguments(self, parser):
        parser.add_argument(
            'name',
            help=_('Имя хранилища (не более 255 символов, должно быть уникальным)')
        )
        parser.add_argument(
            'base_dir',
            help=_('Базовая директория хранилища - путь относительно корня всех хранилищ MMKIT_STORAGES_ROOT_DIR '
                   '(не более 255 символов, должен быть уникальным)')
        )
        parser.add_argument(
            '-i', '--id',
            action='store',
            dest='id',
            default=None,
            help=_('Если параметр присутствует, то хранилище будет создано с указанным в нём UUID в качестве ID.')
        )
        parser.add_argument(
            '-w', '--read-write',
            action='store_true',
            dest='read_write',
            default=False,
            help=_('Если флаг отсутствует, то хранилище будет создано только для чтения (см. поле <read_only> модели).')
        )
        parser.add_argument(
            '-c', '--create-dir',
            action='store_true',
            dest='create_dir',
            default=False,
            help=_('Если флаг установлен, то при создании хранилища будет инициализирована и его базовая директория '
                   '(создана новая или перезаписана существующая - см. параметр конфигурации '
                   'MMKIT_STORAGES_FORBID_BASE_REWRITE). Если флаг и директория отсутствуют - будет запущено '
                   'исключение.')
        )
        parser.add_argument(
            '-t', '--test-run',
            action='store_true',
            dest='test_run',
            default=False,
            help=_('Если флаг установлен, то фактически никакие операции с файловой системой и базой данных '
                   'проводиться не будут. Используется для тестовых нужд.')
        )

    def handle(self, *args, **options):
        verbosity = int(options['verbosity'])
        storages_root = os.path.realpath(settings.MMKIT_STORAGES_ROOT_DIR)
        base_dir_abs = os.path.realpath('{}/{}'.format(storages_root, options['base_dir']))
        if verbosity >= 1:
            if options['test_run']:
                print('Установлен флаг -t (--test-run) - ЭТО ТЕСТОВЫЙ ЗАПУСК, НИКАКИЕ ИЗМЕНЕНИЯ НЕ БУДУТ СОХРАНЕНЫ.')
            print(_('Абсолютный путь к корневой директории хранилищ: %(storages_root)s') %
                  {'storages_root': storages_root})
            print(_('Абсолютный путь к базовой директории: %(base_dir_abs)s') % {'base_dir_abs': base_dir_abs})
            if verbosity > 1:
                print(_('Существовует ли корневая директория хранилищ...'))
        if not os.path.isdir(storages_root):
            raise CommandError(storage_exceptions.STORAGES_ROOT_NOT_FOUND % {'root_dir': storages_root})
        if verbosity > 1:
            print(_('Является ли базовая директория хранилища поддиректорией корневой директории хранилищ...'))
        if not fs_utils.in_path(storages_root, base_dir_abs):
            raise CommandError(
                _('Предполагаемая базовая директория хранилища "%(base_dir_abs)s" не является поддиректорией '
                  'корневой директории всех хранилищ "%(storages_root)s".') %
                {'base_dir_abs': base_dir_abs, 'storages_root': storages_root}
            )
        # TODO: также нужно проверить, не попадает ли эта базовая директория внутрь какого-либо хранилища
        if verbosity > 1:
            print(_('Существует ли хранилище с такой же базовой директорией...'))
        base_dir = os.path.relpath(base_dir_abs, storages_root)
        if Storage.objects.filter(base_dir=base_dir).exists():
            raise CommandError(_('Хранилище с такой базовой директорией уже существует.'))
        if verbosity > 1:
            print('Создание экземпляра модели хранилища...')
        s = Storage(id=options['id'] if options['id'] else None, name=options['name'], base_dir=base_dir,
                    read_only=not options['read_write'])
        if verbosity > 1:
            print('Валидация модели...')
        s.full_clean()  # TODO: тут надо посмотреть - что оно там выдаёт в качестве ошибки
        if s.id:
            if verbosity > 1:
                print(_('Для нового хранилища принудительно установлен ID - проверка существования...'))
            if Storage.objects.filter(id=s.id).exists():
                raise CommandError(_('Хранилище с ID %(id)s уже существует.') % {'id': s.id})
        if verbosity > 1:
            print(_('Проверка существования базовой директории хранилища...'))
        if not os.path.isdir(base_dir_abs):
            if verbosity >= 1:
                print(_('Базовая директория не существует'))
            if not options['create_dir']:
                raise CommandError(
                    _('Базовая директория не существует. Если вы хотите, чтобы она была инициализирована '
                      'автоматически - используйте флаг -c (--create-dir).')
                )
            else:
                if verbosity >= 1:
                    print(_('Установлен флаг -c (--create-dir) - инициализируем базовую директорию...'))
                if not options['test_run']:
                    s.init_storage_base()
        if not options['test_run']:
            s.save(force_insert=True)  # TODO: здесь нужно добавить удаление созданной папки, если что-то пошло не так
        if verbosity >= 1:
            print(_('Хранилище создано.'))


