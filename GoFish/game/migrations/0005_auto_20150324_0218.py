# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20150323_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='pool',
            name='gameLobbyID',
            field=models.ForeignKey(default=0, to='game.Game'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='game',
            name='gameStarted',
            field=models.TimeField(default=datetime.datetime(2015, 3, 24, 2, 8, 11, 170851)),
        ),
    ]
