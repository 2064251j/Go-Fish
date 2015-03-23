# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20150323_2143'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='rank',
            field=models.CharField(default=b'', max_length=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='suit',
            field=models.CharField(default=b'', max_length=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='gameStarted',
            field=models.TimeField(default=datetime.datetime(2015, 3, 23, 21, 46, 19, 131000)),
        ),
    ]
