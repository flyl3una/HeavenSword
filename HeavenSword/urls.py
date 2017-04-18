"""HeavenSword URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import xadmin
from django.conf.urls import url, include
from django.contrib import admin

from web import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^admin/', include(xadmin.site.urls)),
    url(r'^index/$', views.index),
    url(r'^$', views.index),
    url(r'^user/captcha/$', views.captcha),
    url(r'^user/login/$', views.user_login),
    url(r'^user/logout/$', views.user_logout),
    url(r'^user/register/$', views.user_register),
    url(r'^user/activate/(.*)/$', views.user_activate),
    url(r'^user/find_pwd/$', views.user_find_pwd),
    url(r'^user/info/$', views.user_info),
    url(r'^user/reset_pwd/$', views.user_reset_pwd_post),
    url(r'^user/reset_pwd/(.*)/$', views.user_reset_pwd),

    # url(r'^batch/$', views.batch),
    url(r'^operation/$', views.operation),
    url(r'^help/$', views.help),

    #web
    url(r'^new_single_web_task/$', views.new_single_web_task),
    url(r'^new_batch_web_task/$', views.new_batch_web_task),
    url(r'^view_web_task_list/$', views.view_web_task_list),
    #sys
    # url(r'^new_single_sys_task/$', views.new_single_sys_task),
    # url(r'^new_batch_sys_task/$', views.new_batch_sys_task),
    # url(r'^view_sys_task_list/$', views.view_sys_task_list),

    #info_collection
    url(r'^tools/finger/$', views.finger),
    url(r'^tools/port_scan/$', views.port_scan),
    url(r'^tools/web_spider/$', views.web_spider),
    url(r'^tools/domain_brute/$', views.domain_brute),
    url(r'^tools/port_scan/(\d+)/$', views.view_port_scan),
    url(r'^tools/domain_brute/(\d+)/$', views.view_domain_brute),
    url(r'^tools/web_spider/(\d+)/$', views.view_web_spider),

    # url(r'^task_list/$', views.task_list),
    # url(r'^show_task/', views.show_task),
    url(r'^web_task_info/(\d+)/$', views.web_task_info),

]
