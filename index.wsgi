#coding:utf-8
import sae

from bbs_pro import wsgi                         

application = sae.create_wsgi_app(wsgi.application)
