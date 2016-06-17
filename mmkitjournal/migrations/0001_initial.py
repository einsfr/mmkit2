# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-17 16:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityRecord',
            fields=[
                ('id', models.BigIntegerField(editable=False, primary_key=True, serialize=False)),
                ('dt', models.DateTimeField(auto_now=True, db_index=True)),
                ('object_id', models.BigIntegerField(db_index=True, editable=False)),
                ('message', models.TextField()),
                ('content_type', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='contenttypes.ContentType')),
            ],
            options={
                'default_permissions': (),
                'verbose_name': 'запись в журнале активности',
                'verbose_name_plural': 'записи в журнале активности',
            },
        ),
        migrations.CreateModel(
            name='MessageClass',
            fields=[
                ('id', models.PositiveSmallIntegerField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(editable=False, help_text='Название класса сообщения', max_length=32, verbose_name='название')),
                ('description', models.CharField(editable=False, help_text='Описание класса сообщения', max_length=255, verbose_name='описание')),
            ],
            options={
                'default_permissions': (),
                'verbose_name': 'класс сообщения в журнале активности',
                'verbose_name_plural': 'классы сообщений в журнале активности',
            },
        ),
        migrations.AddField(
            model_name='activityrecord',
            name='message_class',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='messages', to='mmkitjournal.MessageClass'),
        ),
        migrations.AddField(
            model_name='activityrecord',
            name='user',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
