#coding: utf-8
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sae.const 
MYSQL_DB = sae.const.MYSQL_DB 
MYSQL_USER = sae.const.MYSQL_USER 
MYSQL_PASS = sae.const.MYSQL_PASS 
MYSQL_HOST_M = sae.const.MYSQL_HOST 
MYSQL_HOST_S = sae.const.MYSQL_HOST_S 
MYSQL_PORT = sae.const.MYSQL_PORT

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['.sinaapp.com']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bbs',
    #'debugtools',
    'captcha',
    'django.contrib.humanize'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'bbs_pro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bbs_pro.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': MYSQL_DB, 
        'USER': MYSQL_USER, 
        'PASSWORD': MYSQL_PASS, 
        'HOST': MYSQL_HOST_M, 
        'PORT': MYSQL_PORT, 
    }
}
# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'common_static'),
    )

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


#   email
EMAIL_HOST = ''                   #SMTP地址
EMAIL_PORT = 25                                 #SMTP端口
EMAIL_HOST_USER = ''       #我自己的邮箱
EMAIL_HOST_PASSWORD = ''                  #我的邮箱密码
EMAIL_SUBJECT_PREFIX = u'[django]'            #为邮件Subject-line前缀,默认是'[django]'
EMAIL_USE_TLS = True                             #与SMTP服务器通信时，是否启动TLS链接(安全链接)。默认是false
#管理员站点
SERVER_EMAIL = ''            #The email address that error messages come from, such as those sent to ADMINS and MANAGERS.
DEFAULT_FROM_EMAIL = ""

#FILE_CHARSET = 'gb18030'
DEFAULT_CHARSET = 'utf-8'


CAPTCHA_OUTPUT_FORMAT = u'%(text_field)s %(hidden_field)s %(image)s'  
# 噪点样式  
CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_null', # 没有样式  
     'captcha.helpers.noise_arcs', # 线  
    # 'captcha.helpers.noise_dots', # 点  
)  
# 图片大小  
CAPTCHA_IMAGE_SIZE = (100, 25)  
CAPTCHA_BACKGROUND_COLOR = '#ffffff'  
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge' # 图片中的文字为随机英文字母，如 mdsh  
# CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'    # 图片中的文字为数字表达式，如1+2=</span>  
  
CAPTCHA_LENGTH = 4 # 字符个数  
CAPTCHA_TIMEOUT = 1 # 超时(minutes)  
