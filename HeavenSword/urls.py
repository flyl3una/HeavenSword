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
    url(r'^user/login/$', views.user_login),
    url(r'^user/logout/$', views.user_logout),
    url(r'^user/register/$', views.user_register),
    url(r'^user/activate/(.*)/$', views.user_activate),

    url(r'^batch/$', views.batch),
    url(r'^operation/$', views.operation),
    url(r'^about/$', views.about),
    url(r'^one/$', views.one),

    #task
    url(r'^new_single_task/$', views.new_single_task),
    url(r'^new_batch_task/$', views.new_batch_task),
    url(r'^view_all_task/$', views.view_all_task),
    url(r'^view_single_task/$', views.view_single_task),
    url(r'^view_batch_task/$', views.view_batch_task),

    url(r'^task_list/$', views.task_list),
    url(r'^show_task/', views.show_task),
    url(r'^task_info/(\d+)/$', views.task_info),

    # scan
    url(r'^scan/finger', views.finger),
    url(r'^scan/port_scan', views.port_scan),
    url(r'^scan/exploit_attack', views.exploit_attack),
    url(r'^scan/spider', views.spider),
    url(r'^scan/domain_brute', views.domain_brute),
]
