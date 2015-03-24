# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_auto_20150324_0221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='gameStarted',
            field=models.BooleanField(default=False),
        ),
    ]
