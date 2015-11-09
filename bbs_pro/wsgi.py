"""
WSGI config for bbs_pro project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os, sys
root = os.path.dirname(__file__)                                             
sys.path.insert(0, os.path.join(root, '..', 'site-packages'))       
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bbs_pro.settings")

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bbs_pro.settings")

application = get_wsgi_application()
