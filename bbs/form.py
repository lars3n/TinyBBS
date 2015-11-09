#coding:utf-8
from django import forms
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField

from .models import Category

class CaptchaForm(forms.Form):
    captcha = CaptchaField()


class LoginForm(forms.Form):
    """LoginForm"""
    username = forms.CharField(
        label='用户名', max_length=30)
    password = forms.CharField(
        label='密码', max_length=30,
        widget=forms.PasswordInput)
    captcha = CaptchaField(
        label='验证码')


class RegisterForm(forms.Form):
    username = forms.CharField(
        label="用户名", 
        max_length=30)
    email = forms.EmailField(
        label="Email",
        max_length=100)
    password1 = forms.CharField(
        label='密码', 
        min_length=3, max_length=30,
        widget=forms.PasswordInput,)
    password2 = forms.CharField(
        label='再次输入密码', 
        min_length=3, max_length=30,
        widget=forms.PasswordInput,)
    captcha = CaptchaField(
        label='验证码')


class BbsPubForm(forms.Form):
    bbs_title = forms.CharField(
        label="标题", 
        #min_length=5,
        max_length=50)
    bbs_content = forms.CharField(
        label="内容",
        #min_length=10,
        max_length=10000,
        widget=forms.Textarea)
    bbs_category = forms.ModelChoiceField(
        label="类别",
        queryset=Category.objects.all(),
        required=True, )
    captcha = CaptchaField(
        label='验证码')


class ForgotForm(forms.Form):
    email = forms.EmailField(
        label="Email", max_length=100)
    captcha = CaptchaField(
        label='验证码')


class ResetPwdForm(forms.Form):
    """docstring for ResetPwdForm"""
    password1 = forms.CharField(
        label='密码', 
        min_length=3, max_length=30,
        widget=forms.PasswordInput,)

    password2 = forms.CharField(
        label='再次输入密码', 
        min_length=3, max_length=30,
        widget=forms.PasswordInput,)


class ChangeInfoForm(forms.Form):
    signature = forms.CharField(
        label="签名",
        max_length=200,
        widget=forms.Textarea)
    user_intro = forms.CharField(
        label="简介",
        max_length=512,
        widget=forms.Textarea)


class ChangeAvatarForm(forms.Form):
    avatar = forms.FileField(
        label="头像")


class ChangePwdForm(forms.Form):
    ori_password = forms.CharField(
        label='原密码', 
        min_length=3, max_length=30,
        widget=forms.PasswordInput,)
    new_password_1 = forms.CharField(
        label='新密码', 
        min_length=3, max_length=30,
        widget=forms.PasswordInput,)
    new_password_2 = forms.CharField(
        label='再次输入新密码', 
        min_length=3, max_length=30,
        widget=forms.PasswordInput,)


class ReplayForm(forms.Form):
    content = forms.CharField(
        #min_length = 10,
        max_length=200,
        widget=forms.Textarea)


class MessageForm(forms.Form):
    content = forms.CharField(
        #min_length = 10,
        max_length=200,
        widget=forms.Textarea)