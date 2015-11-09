# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bbs_user',
            name='favorites',
            field=models.ManyToManyField(related_name='FavorBbs', null=True, to='bbs.BBS', blank=True),
        ),
    ]
