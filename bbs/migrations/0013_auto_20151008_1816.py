# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0012_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='bbs_user',
            name='user_intro',
            field=models.TextField(default=b'\xe8\xbf\x99\xe4\xb8\xaa\xe5\xae\xb6\xe4\xbc\x99\xe7\x9c\x9f\xe7\x9a\x84\xe5\xbe\x88\xe6\x87\x92~~', max_length=512),
        ),
        migrations.AlterField(
            model_name='bbs_user',
            name='signature',
            field=models.CharField(default=b'\xe8\xbf\x99\xe4\xb8\xaa\xe5\xae\xb6\xe4\xbc\x99\xe5\xbe\x88\xe6\x87\x92~~', max_length=128),
        ),
    ]
