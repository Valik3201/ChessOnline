# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-23 15:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Chess', '0003_game_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='draws',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='game',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 5, 23, 15, 57, 2, 269304)),
        ),
    ]