# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_auto_20150324_0218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='gameStarted',
            field=models.TimeField(default=datetime.datetime(2015, 3, 24, 2, 21, 53, 296625)),
        ),
    ]
