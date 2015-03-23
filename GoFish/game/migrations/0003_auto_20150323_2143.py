# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_game_gamestarted'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='gameCreator',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='gameStarted',
            field=models.TimeField(default=datetime.datetime(2015, 3, 23, 21, 43, 49, 872000)),
        ),
    ]
