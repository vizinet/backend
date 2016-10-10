# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-27 06:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_upload', '0006_auto_20160921_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='lowX',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='picture',
            name='lowY',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='picture',
            name='pictureWithCircles',
            field=models.ImageField(blank=True, null=True, upload_to='static/circles/'),
        ),
        migrations.AlterField(
            model_name='picture',
            name='geoX',
            field=models.FloatField(default=46.7298),
        ),
        migrations.AlterField(
            model_name='picture',
            name='geoY',
            field=models.FloatField(default=-117.181738),
        ),
    ]
