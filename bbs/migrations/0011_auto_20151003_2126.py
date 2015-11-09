# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0010_message_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
