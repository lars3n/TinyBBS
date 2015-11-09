#coding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.core.paginator import Paginator

class CateClass(models.Model):
    class_name = models.CharField(max_length=32, unique=True)

    def __unicode__(self):
        return self.class_name


class Category(models.Model):
    category_name = models.CharField(max_length=32, unique=True)
    category_admin = models.ForeignKey('BBS_user')
    category_class = models.ForeignKey('CateClass', default=1)

    def __unicode__(self):
        return self.category_name


class BBS(models.Model):
    bbs_title = models.CharField(max_length=64)
    bbs_summary = models.CharField(max_length=256, blank=True, null=True)
    bbs_content = models.TextField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    view_count = models.IntegerField()
    bbs_author = models.ForeignKey('BBS_user')
    bbs_category = models.ForeignKey('Category')

    class Meta:
        ordering = ['-created_at']

    def __unicode__(self):
        return self.bbs_title


class Comments(models.Model):
    bbs_id = models.ForeignKey('BBS')
    user_id = models.ForeignKey('BBS_user')
    cmt_content = models.TextField(max_length=512)
    pub_date = models.DateTimeField()

    def __unicode__(self):
        return self.cmt_content 


class BBS_user(models.Model):
    user = models.OneToOneField(User)
    favorites = models.ManyToManyField('BBS', related_name="FavorBbs", 
                                        null=True, blank=True, default=None)
    signature = models.CharField(max_length=128, default="这个家伙很懒~~")
    avatar = models.ImageField(upload_to="avatar/",
                                default="avatar/default_avatar.jpg")
    # 这个字段用于重置密码
    reset_password = models.CharField(max_length=100, blank=True, null=True)
    user_intro = models.TextField(max_length=512, default="这个家伙真的很懒~~")

    def __unicode__(self):
        return self.user.username

'''站内私信系列表'''
class Message(models.Model):
    msg_content = models.OneToOneField('MsgContent',)
    msg_from = models.ForeignKey('BBS_user', related_name='msg_from')
    msg_to = models.ForeignKey('BBS_user', related_name='msg_to')
    dialog = models.ForeignKey('MsgDialog',)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.msg_content.message_text


class MsgDialog(models.Model):

    def __unicode__(self):
        return self.id

class MsgContent(models.Model):
    message_text = models.TextField(max_length=512)

    def __unicode__(self):
        return self.message_text


class Follow(models.Model):
    follow = models.ManyToManyField('BBS_user', related_name='follow',
        null=True, blank=True, default=None)
    fans = models.ManyToManyField('BBS_user', related_name='fans',
        null=True, blank=True, default=None)

    def __unicode__(self):
        return self.id