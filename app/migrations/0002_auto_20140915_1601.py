# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario_detalles',
            old_name='id',
            new_name='usuario_detalles',
        ),
        migrations.RenameField(
            model_name='usuario_extra',
            old_name='id',
            new_name='usuario_extra',
        ),
        migrations.AddField(
            model_name='pregunta',
            name='tags',
            field=models.ManyToManyField(to='app.tag'),
            preserve_default=True,
        ),
    ]
