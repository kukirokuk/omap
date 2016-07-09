# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-09 19:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0002_auto_20160709_1938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='room_count',
        ),
        migrations.AddField(
            model_name='room',
            name='emp_number',
            field=models.CharField(blank=True, max_length=256, verbose_name='Count of places'),
        ),
    ]
