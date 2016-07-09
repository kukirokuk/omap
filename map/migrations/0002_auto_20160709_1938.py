# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-09 19:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='count',
        ),
        migrations.AddField(
            model_name='room',
            name='room_count',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Count of places'),
        ),
    ]
