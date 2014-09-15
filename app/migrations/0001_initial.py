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
            name='Comentario',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('autor', models.CharField(max_length=20)),
                ('contenido', models.TextField()),
                ('n_votos', models.IntegerField(default=0)),
                ('estado', models.CharField(max_length=2)),
                ('fecha_hora', models.DateField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('titulo', models.CharField(max_length=100)),
                ('contenido', models.TextField()),
                ('n_vistas', models.PositiveIntegerField(default=0)),
                ('n_respuestas', models.PositiveIntegerField(default=0)),
                ('n_votos', models.IntegerField(default=0)),
                ('respondido', models.BooleanField(default=False)),
                ('estado', models.CharField(max_length=2)),
                ('fecha_hora', models.DateField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('contenido', models.TextField()),
                ('n_votos', models.IntegerField(default=0)),
                ('mejor', models.BooleanField(default=False)),
                ('estado', models.CharField(default=b'OP', max_length=2)),
                ('fecha_hora', models.DateField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=25)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserDetalles',
            fields=[
                ('id', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('rol', models.CharField(max_length=1)),
                ('fecha_registro', models.DateField(auto_now_add=True)),
                ('fecha_movimento', models.DateField(auto_now_add=True)),
                ('descripcion', models.CharField(max_length=100)),
                ('puntaje', models.IntegerField(default=0)),
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
            name='pregunta_id',
            field=models.ForeignKey(to='app.Pregunta'),
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
            name='id_pregunta',
            field=models.ForeignKey(to='app.Pregunta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comentario',
            name='id_respuesta',
            field=models.ForeignKey(to='app.Respuesta'),
            preserve_default=True,
        ),
    ]
