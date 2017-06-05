# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('file_upload', '0011_auto_20170511_2112'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(default='', blank=True)),
                ('picture', models.ForeignKey(default=-1, to='file_upload.picture')),
                ('user', models.ForeignKey(default=-1, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
