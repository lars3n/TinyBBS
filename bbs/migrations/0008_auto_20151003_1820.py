# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0007_auto_20151003_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='dialog',
            field=models.ForeignKey(to='bbs.MsgDialog'),
        ),
        migrations.AlterField(
            model_name='message',
            name='msg_content',
            field=models.OneToOneField(to='bbs.MsgContent'),
        ),
    ]
