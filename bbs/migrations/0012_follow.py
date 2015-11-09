# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0011_auto_20151003_2126'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fans', models.ManyToManyField(default=None, related_name='fans', null=True, to='bbs.BBS_user', blank=True)),
                ('follow', models.ManyToManyField(default=None, related_name='follow', null=True, to='bbs.BBS_user', blank=True)),
            ],
        ),
    ]
