# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_auto_20150324_1555'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='cardID',
        ),
        migrations.AddField(
            model_name='hand',
            name='playerID',
            field=models.ForeignKey(default=0, to='game.Player'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='lobbyID',
            field=models.ForeignKey(default=0, to='game.Game'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pool',
            name='lobbyID',
            field=models.ForeignKey(default=0, to='game.Game'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='game',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
        ),
        migrations.AlterField(
            model_name='hand',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
        ),
        migrations.AlterField(
            model_name='pool',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
        ),
    ]
