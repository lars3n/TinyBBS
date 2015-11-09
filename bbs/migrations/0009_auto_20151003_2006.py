# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0008_auto_20151003_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bbs_user',
            name='reset_password',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
