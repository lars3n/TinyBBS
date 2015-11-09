# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0005_auto_20151003_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 3, 6, 25, 43, 191000, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
