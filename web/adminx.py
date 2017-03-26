# coding=utf-8

from django.contrib.auth.models import User
from xadmin.plugins.batch import BatchChangeAction

from web.models import WebSingleTask, Finger, WebExploit, PortScan
from xadmin.views import CommAdminView

import xadmin
# from models import UserSettings
from xadmin.layout import *


class UserSettingsAdmin(object):
    model_icon = 'fa fa-cog'
    hidden_menu = True


class GlobalSetting(object):

    #设置base_site.html的Title
    site_title = '倚天剑'

    #设置base_site.html的Footer
    site_footer = '倚天屠龙记'

    # 菜单设置
    # def get_site_menu(self):
    #     return (
            # {'title': 'web项目',
            #  'perm': self.get_model_perm(User, 'change'),
            #  'menus': ({'title': 'web任务', 'url': self.get_model_url(WebSingleTask, 'changelist')},
            #            {'title': '指纹识别', 'url': self.get_model_url(Finger, 'changelist')},
            #            {'title': 'exp测试', 'url': self.get_model_url(WebExploit, 'changelist')})
            #  },
            # {'title': '分类管理', 'perm': self.get_model_perm(Category, 'change'), 'menus': (
            #     {'title': '主要分类', 'url': self.get_model_url(Category, 'changelist') + '?_p_parent__isnull=True'},
            #     {'title': '游戏资料', 'url': self.get_model_url(Category, 'changelist') + '?_rel_parent__id__exact=2'},
            # )},
        # )


class WebSingleTaskAdmin(object):
    list_display = ('id', 'target_url', 'domain', 'status', 'finger_id', 'exploit_id', 'update_date')
    list_display_links = ('domain',)
    # wizard_
    search_fields = ['domain']
    # actions = [BatchChangeAction, ]
    batch_fields = ('contact',)


class FingerAdmin(object):
    list_display = ('id', 'target_domain', 'target_url', 'status', 'finger_count', 'current_index', 'update_date')


class PortScanAdmin(object):
    list_display = ('id', 'target_ip', 'status', 'port_count', 'current_index', 'thread', 'model', 'update_date')


xadmin.site.register(CommAdminView, GlobalSetting)
xadmin.site.register(WebSingleTask, WebSingleTaskAdmin)
xadmin.site.register(Finger, FingerAdmin)
xadmin.site.register(PortScan, PortScanAdmin)
# xadmin.site.register(UserSettings, UserSettingsAdmin)
