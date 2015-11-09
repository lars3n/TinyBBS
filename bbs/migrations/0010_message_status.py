# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0009_auto_20151003_2006'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='status',
            field=models.BooleanField(default=0),
        ),
    ]
