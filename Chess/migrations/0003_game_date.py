# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-23 13:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Chess', '0002_auto_20170523_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 5, 23, 13, 55, 58, 108539)),
        ),
    ]