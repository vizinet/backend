# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='submit_date',
            field=models.TextField(default='', blank=True),
        ),
    ]
