# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BBS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bbs_title', models.CharField(max_length=64)),
                ('bbs_summary', models.CharField(max_length=256, null=True, blank=True)),
                ('bbs_content', models.TextField(max_length=10000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('view_count', models.IntegerField()),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='BBS_user',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('signature', models.CharField(default=b'Nothing here', max_length=128)),
                ('avatar', models.ImageField(default=b'avatar/default_avatar.jpg', upload_to=b'avatar/')),
                ('reset_password', models.CharField(max_length=100, null=True)),
                ('favorites', models.ManyToManyField(related_name='FavorBbs', to='bbs.BBS')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CateClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('class_name', models.CharField(unique=True, max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category_name', models.CharField(unique=True, max_length=32)),
                ('category_admin', models.ForeignKey(to='bbs.BBS_user')),
                ('category_class', models.ForeignKey(default=1, to='bbs.CateClass')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cmt_content', models.TextField(max_length=512)),
                ('pub_date', models.DateTimeField()),
                ('bbs_id', models.ForeignKey(to='bbs.BBS')),
                ('user_id', models.ForeignKey(to='bbs.BBS_user')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='MsgContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message_text', models.TextField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='MsgDialog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='dialog',
            field=models.ForeignKey(related_name='msg_dialog', to='bbs.MsgDialog'),
        ),
        migrations.AddField(
            model_name='message',
            name='msg_content',
            field=models.OneToOneField(related_name='msg_content', to='bbs.MsgContent'),
        ),
        migrations.AddField(
            model_name='message',
            name='msg_from',
            field=models.ForeignKey(related_name='msg_from', to='bbs.BBS_user'),
        ),
        migrations.AddField(
            model_name='message',
            name='msg_to',
            field=models.ForeignKey(related_name='msg_to', to='bbs.BBS_user'),
        ),
        migrations.AddField(
            model_name='bbs',
            name='bbs_author',
            field=models.ForeignKey(to='bbs.BBS_user'),
        ),
        migrations.AddField(
            model_name='bbs',
            name='bbs_category',
            field=models.ForeignKey(to='bbs.Category'),
        ),
    ]
