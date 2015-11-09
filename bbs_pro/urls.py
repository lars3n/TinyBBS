#coding:utf-8
from django.conf.urls import include, url, patterns
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from bbs import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r"^captcha/", include('captcha.urls')),

    # 用於ajax刷新驗證碼
    url(r'^new_captcha/$', views.new_captcha),

    # BBS類
    url(r'^$', views.index, name="home"),   
    url(r"^category/(\d+)$", views.category, name='category'),
    url(r"^bbs/bbs_pub/$", views.bbs_pub, name='bbs_pub'),
    url(r"^bbs/bbs_detail/(\d+)/(\d)*/$", 'bbs.views.bbs_detail', name='bbs_detail'),
    url(r"^bbs/recent/(\d+)/$", views.recent, name="recent"),
    url(r"^bbs/delete/(\d+)/$", views.delete, name="bbs_delete"),
    url(r"^bbs/replays/(\d+)/$", views.replays, name="replays"),
 
    # 用戶賬戶類   
    url(r"^accounts/login/$", views.login, name='login'),
    url(r"^accounts/register/$", views.register, name="register"),
    url(r"^accounts/logout/$", views.logout, name='logout'),
    url(r"^accounts/forgot/$", views.forgot, name='forgot'),
    url(r"^accounts/reset_password/([a-z0-9]+)/$", views.reset, name="reset_password"),

    # 用戶設置類
    url(r"^settings/change_info/$", views.change_info, name='change_info'),
    url(r"^settings/change_avatar/$", views.change_avatar, name='change_avatar'),
    url(r"^settings/change_password/$", views.change_password, name="change_password"), 
    url(r'^settings/info/$', views.info, name="info"),        # 用於發送成功修改的頁面

    # 用戶功能類
    url(r"^user/(\d+)$", views.user_profile, name="user_profile"),
    url(r'^user/favorites/$', views.favorites, name="favorites"),
    url(r'^user/favorite/add/(\d+)/$', views.favor_add, name="favor_add"),
    url(r'^user/favorite/del/(\d+)/$', views.favor_del, name="favor_del"),
    url(r'^user/message/$', views.message, name="message"),
    url(r'^user/message/send/(\d+)/$', views.message_send, name="message_send"),
    url(r'^user/message/show/(\d+)/$', views.message_show, name="message_show"),
    url(r'^user/follow/$', views.follow, name="follow"),
    url(r'^user/follow/add/(\d+)/$', views.follow_add, name="follow_add"),
    url(r'^user/follow/del/(\d+)/$', views.follow_del, name="follow_del"),
    url(r'^user/fans/$', views.fans, name="fans"),
    url(r'^search/$', views.search, name="search"),

    url(r'^images/(?P<path>.*)','django.views.static.serve',{'document_root':'/'}),
]

#if settings.DEBUG:
if True:       #在生产环境下使用django来处理静态文件，django并不建议这样做
    '''
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    '''
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
    )
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
