import importlib

from django.core.management.base import BaseCommand
from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mmkitjournal.models import MessageClass


class Command(BaseCommand):
    help = _('Загружает классы сообщений для журнала активности')

    MSGCLASSES_MODULE = 'msgclasses'
    MSGCLASSES_DICT_VAR = 'msg_classes'

    def handle(self, *args, **options):
        for app_config in apps.get_app_configs():
            try:
                module = importlib.import_module('{}.{}'.format(app_config.module.__name__, self.MSGCLASSES_MODULE))
            except ImportError:
                continue
            msg_classes_dict = getattr(module, self.MSGCLASSES_DICT_VAR)
            for (i, t) in msg_classes_dict.items():
                name, description = t
                MessageClass(id=i, name=name, description=description).save()
