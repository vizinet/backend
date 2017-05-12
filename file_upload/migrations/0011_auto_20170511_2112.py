# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_upload', '0010_auto_20161117_0234'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='radiusHigh',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='picture',
            name='radiusLow',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='picture',
            name='algorithmType',
            field=models.TextField(default='near_far', null=True),
        ),
    ]
