# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_upload', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='algorithmone',
            old_name='farTargetDistance',
            new_name='farDistance',
        ),
        migrations.RenameField(
            model_name='algorithmone',
            old_name='nearTargetDistance',
            new_name='nearDistance',
        ),
        migrations.AlterField(
            model_name='picture',
            name='algorithmType',
            field=models.TextField(default='AlgorithmOne'),
        ),
    ]
