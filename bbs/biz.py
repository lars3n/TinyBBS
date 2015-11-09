#coding:utf-8
import time
import hashlib
from threading import Timer

from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse

from .models import *
from django.conf import settings

class UserBiz(object):
    """docstring for UserBiz"""
    def userValidate(self, form):
        el = ErrorList()
        username = form['username'].value()
        password1 = form['password1'].value()
        password2 = form['password2'].value()
        email = form['email'].value()

        username_exists = self.getUserByUserName(username)
        email_exists = self.getUserByEmail(email)
        error_dict = {}
        if username_exists:               
            error_dict['username'] = "用户名已注册"

        if email_exists:
            error_dict['email'] = "邮箱已注册"

        if password1 != password2:
            error_dict['password2'] = '两次密码不一致'
        return error_dict

    def getUserByUserName(self, username):
        """If the user doesn't exists, return a None type"""
        try:           
            username_exists = User.objects.get(username=username)
        except:
            username_exists = None
        return username_exists

    def getUserByEmail(self, email):
        """If the user doesn't exists, return a None type"""
        try:
            email_exists = User.objects.get(email=email)
        except:
            email_exists = None
        return email_exists

    def save(self,new_user):
        try:
            validMsg = self.validateBeforeSave(new_user)
            if validMsg != '':
                raise "ValidationException", validMsg
            new_user.save()
        except "ValidationException", arg:
            raise "ValidationException", arg
        except Exception, e:
            raise Exception(e)

    def validateBeforeSave(self, new_user):
        validMsg = ''
        if not new_user.username:
            validMsg = '用户名不能为空！'
        if not new_user.email:
            validMsg = validMsg + 'Email地址不能为空！'
        if not new_user.password:
            validMsg = validMsg + '密码不能为空！'
        return validMsg


class BbsBiz(object):
    """docstring for BBSBiz"""
    def getCategory(self, bbs_category):
        try:
            bbs_category = Category.objects.get(category_name=bbs_category)
        except:
            bbs_category = None
        return bbs_category

    def getBbsAuthorByReq(self, request_user):
        try:
            bbs_author = BBS_user.objects.get(user__username=request_user)
        except:
            bbs_author = None
        return bbs_author


class ResetPwdBiz(object):
    """A Class handle the password reset business"""
    def make_reset_url(self, email):
        """This method must be user only once because of the timeStr"""
        salt = 'A9d2qc'
        timeStr = str(time.time())
        reset_url = hashlib.md5(salt + email + timeStr).hexdigest()
        return reset_url

    def send_email(self, toEmail):
        for i in settings.ALLOWED_HOSTS:
            if i == "localhost":
                HOST = "localhost:8000"
            else:
                HOST = i

        reset_url = self.make_reset_url(toEmail)
        subject, from_email, to = 'blog-message', settings.EMAIL_HOST_USER, toEmail
        text_content = 'This is an validate message'
        html_content = u'<h1>请将下面链接复制到浏览器地址栏打开，该链接十分钟后失效</h1>\
            <a href="{0}/accounts/reset_password/{1}">\
            {0}/accounts/reset_password/{1}</a>'.format(HOST, reset_url)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
        self.save_reset_url(reset_url, toEmail)

    def save_reset_url(self, resetUrl, email):
        user = BBS_user.objects.get(user__email=email)
        user.reset_password = resetUrl
        user.save()
        # 在一定时间后删除用户的验证的URL
        t = Timer(600,  self.delete_reset_url, ( user, ))
        t.start()

    def delete_reset_url(self, userObj):
        userObj.reset_password = ''
        userObj.save()  

