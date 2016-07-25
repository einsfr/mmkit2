# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-22 19:57
from __future__ import unicode_literals

import django.contrib.postgres.fields
import django.contrib.postgres.fields.hstore
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Имя хранилища (не более 255 символов, должно быть уникальным)', max_length=255, unique=True, verbose_name='имя')),
                ('base_dir', models.CharField(help_text='Базовая директория хранилища - путь относительно корня всех хранилищ MMKIT_STORAGES_ROOT_DIR (не более 255 символов, должен быть уникальным)', max_length=255, unique=True, verbose_name='корневая директория')),
                ('access_protocols', django.contrib.postgres.fields.hstore.HStoreField(blank=True, default={}, help_text='Словарь, содержащий пары вида <протокол_доступа>: <базовая часть URL для доступа> (по-умолчанию - пустой)', verbose_name='Протоколы доступа')),
                ('read_only', models.BooleanField(default=True, help_text='Если True - хранилище можно использовать только для чтения (по-умолчанию - True)', verbose_name='только для чтения')),
                ('allowed_usage', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=32), blank=True, default=[], help_text='Массив разрешённых вариантов использования хранилища (по-умолчанию - пустой)', size=None, verbose_name='Разрешённые варианты использования')),
            ],
            options={
                'default_permissions': (),
                'verbose_name': 'хранилище',
                'verbose_name_plural': 'хранилища',
            },
        ),
    ]