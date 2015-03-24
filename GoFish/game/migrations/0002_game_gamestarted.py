# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='gameStarted',
            field=models.TimeField(default=datetime.datetime(2015, 3, 23, 21, 42, 36, 56000)),
            preserve_default=True,
        ),
    ]
