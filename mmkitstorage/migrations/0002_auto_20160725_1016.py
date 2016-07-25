# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-25 07:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('mmkitstorage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StorageObject',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('path', models.CharField(help_text='Путь к объекту относительно корня хранилища (не более 255 символов)', max_length=255, verbose_name='путь к объекту')),
                ('storage', models.ForeignKey(help_text='Хранилище, в котором размещается объект', on_delete=django.db.models.deletion.CASCADE, related_name='stored_objects', to='mmkitstorage.Storage', verbose_name='хранилище')),
            ],
            options={
                'verbose_name_plural': 'объекты в хранилищах',
                'verbose_name': 'объект в хранилище',
                'default_permissions': (),
            },
        ),
        migrations.AlterUniqueTogether(
            name='storageobject',
            unique_together=set([('storage', 'path')]),
        ),
    ]
