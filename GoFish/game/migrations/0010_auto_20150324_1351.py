# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0009_auto_20150324_0243'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='score',
        ),
        migrations.AddField(
            model_name='player',
            name='score',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
