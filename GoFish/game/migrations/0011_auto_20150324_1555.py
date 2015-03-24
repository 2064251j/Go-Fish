# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0010_auto_20150324_1351'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='gameCreator',
            new_name='creator',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='gameLobbyID',
            new_name='lobbyID',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='gameStarted',
            new_name='started',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='gameLobbyID',
            new_name='lobbyID',
        ),
        migrations.RenameField(
            model_name='pool',
            old_name='gameLobbyID',
            new_name='lobbyID',
        ),
        migrations.AddField(
            model_name='game',
            name='turn',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
