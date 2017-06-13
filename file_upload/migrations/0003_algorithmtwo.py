# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_upload', '0002_auto_20170609_1847'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlgorithmTwo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image2', models.ImageField(upload_to='pictures/')),
                ('calculatedVisualRange', models.FloatField(default=0, null=True)),
                ('farX', models.FloatField(default=0)),
                ('farY', models.FloatField(default=0)),
                ('nearX', models.FloatField(default=0)),
                ('nearY', models.FloatField(default=0)),
                ('farRadius', models.FloatField(null=True)),
                ('nearRadius', models.FloatField(null=True)),
                ('farDistance', models.FloatField(default=0, null=True)),
                ('nearDistance', models.FloatField(default=0, null=True)),
                ('picture', models.ForeignKey(to='file_upload.Picture', unique=True)),
            ],
        ),
    ]
