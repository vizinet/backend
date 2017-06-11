# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AlgorithmOne',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('calculatedVisualRange', models.FloatField(default=0, null=True)),
                ('farX', models.FloatField(default=0)),
                ('farY', models.FloatField(default=0)),
                ('nearX', models.FloatField(default=0)),
                ('nearY', models.FloatField(default=0)),
                ('farRadius', models.FloatField(null=True)),
                ('nearRadius', models.FloatField(null=True)),
                ('farTargetDistance', models.FloatField(default=0, null=True)),
                ('nearTargetDistance', models.FloatField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to='pictures/')),
                ('thumbnail', models.ImageField(null=True, upload_to='thumbnails/', blank=True)),
                ('uploadTime', models.DateTimeField(default=datetime.datetime.now)),
                ('description', models.TextField(default=' ', null=True)),
                ('algorithmType', models.TextField(default='AlgorithmOne', null=True)),
                ('eVisualRange', models.FloatField(default=0)),
                ('vrUnits', models.CharField(default='K', max_length=1, null=True)),
                ('geoX', models.FloatField(default=46.7298)),
                ('geoY', models.FloatField(default=-117.181738)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('picture', models.ForeignKey(to='file_upload.Picture')),
            ],
        ),
        migrations.AddField(
            model_name='algorithmone',
            name='picture',
            field=models.ForeignKey(to='file_upload.Picture', unique=True),
        ),
    ]
