# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0002_auto_20151003_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='created_at',
            field=models.DateTimeField(default=None),
        ),
        migrations.AlterField(
            model_name='bbs_user',
            name='favorites',
            field=models.ManyToManyField(default=None, related_name='FavorBbs', null=True, to='bbs.BBS', blank=True),
        ),
    ]
