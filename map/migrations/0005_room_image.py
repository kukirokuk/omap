# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-11 12:22
from __future__ import unicode_literals

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0004_auto_20160711_0842'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, null=True, upload_to=b'photo/'),
        ),
    ]
