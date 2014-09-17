# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20140915_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='fecha_hora',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='pregunta',
            name='fecha_hora',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='respuesta',
            name='fecha_hora',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
