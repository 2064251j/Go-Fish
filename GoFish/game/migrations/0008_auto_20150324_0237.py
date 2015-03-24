# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_auto_20150324_0227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='gameCreator',
            field=models.TextField(default=None, null=True),
        ),
    ]
