# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contenido', models.TextField()),
                ('n_votos', models.IntegerField(default=0)),
                ('estado', models.SmallIntegerField(default=0, max_length=1, choices=[(0, b'Por Detecto'), (1, b'Estado1'), (2, b'Estado2')])),
                ('fecha_hora', models.DateField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='pregunta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=100)),
                ('contenido', models.TextField()),
                ('n_vistas', models.PositiveIntegerField(default=0)),
                ('n_respuestas', models.PositiveIntegerField(default=0)),
                ('n_votos', models.IntegerField(default=0)),
                ('respondido', models.BooleanField(default=False)),
                ('estado', models.SmallIntegerField(default=0, max_length=1, choices=[(0, b'Por Detecto'), (1, b'Estado1'), (2, b'Estado2')])),
                ('fecha_hora', models.DateField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='respuesta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contenido', models.TextField()),
                ('n_votos', models.IntegerField(default=0)),
                ('mejor', models.BooleanField(default=False)),
                ('estado', models.SmallIntegerField(default=0, max_length=1, choices=[(0, b'Por Detecto'), (1, b'Estado1'), (2, b'Estado2')])),
                ('fecha_hora', models.DateField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=25)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='usuario_detalles',
            fields=[
                ('id', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('descripcion', models.CharField(max_length=255, verbose_name=b'Descripci\xc3\xb3n', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='usuario_extra',
            fields=[
                ('id', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('rol', models.CharField(max_length=1, verbose_name=b'Rol')),
                ('puntaje', models.IntegerField(default=0, verbose_name=b'Puntaje')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='respuesta',
            name='autor',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='respuesta',
            name='pregunta',
            field=models.ForeignKey(to='app.pregunta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pregunta',
            name='autor',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comentario',
            name='autor',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comentario',
            name='pregunta',
            field=models.ForeignKey(to='app.pregunta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comentario',
            name='respuesta',
            field=models.ForeignKey(to='app.respuesta'),
            preserve_default=True,
        ),
    ]
