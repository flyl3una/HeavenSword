# coding=utf-8
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from xadmin import AdminSite
from xadmin.plugins.batch import BatchChangeAction

from web.models import WebSingleTask, Finger, WebProof, PortScan
from xadmin.views import CommAdminView
from web.models import *

import xadmin
# from models import UserSettings
from xadmin.layout import *


class UserSettingsAdmin(object):
    model_icon = 'fa fa-cog'
    hidden_menu = True


# class GlobalSetting(object):
#
#     #设置base_site.html的Title
#     site_title = '倚天剑'
#
#     #设置base_site.html的Footer
#     site_footer = '倚天屠龙记'

    # 菜单设置
    # def get_site_menu(self):
    #     return (
            # {'title': 'web项目',
            #  'perm': self.get_model_perm(User, 'change'),
            #  'menus': ({'title': 'web任务', 'url': self.get_model_url(WebSingleTask, 'changelist')},
            #            {'title': '指纹识别', 'url': self.get_model_url(Finger, 'changelist')},
            #            {'title': 'exp测试', 'url': self.get_model_url(WebProof, 'changelist')})
            #  },
            # {'title': '分类管理', 'perm': self.get_model_perm(Category, 'change'), 'menus': (
            #     {'title': '主要分类', 'url': self.get_model_url(Category, 'changelist') + '?_p_parent__isnull=True'},
            #     {'title': '游戏资料', 'url': self.get_model_url(Category, 'changelist') + '?_rel_parent__id__exact=2'},
            # )},
        # )


class WebSingleTaskAdmin(object):
    list_display = ('domain', 'target_url', 'status', 'finger_id', 'proof_id', 'update_date')
    list_display_links = ('domain',)
    # wizard_
    search_fields = ['domain']
    # actions = [BatchChangeAction, ]
    batch_fields = ('contact',)
    # search_fields = ['domain']
    relfield_style = 'fk-ajax'


class FingerAdmin(object):
    list_display = ('target_domain', 'target_url', 'status', 'finger_count', 'current_index', 'update_date')
    search_fields = ['target_domain']


class PortScanAdmin(object):
    list_display = ('target_ip', 'status', 'port_count', 'current_index', 'thread', 'model', 'update_date')
    search_fields = ['target_ip']


class UrlAdmin(object):
    list_display = ('domain', 'url', 'update_date')
    search_fields = ['domain']


class DomainIpAdmin(object):
    list_display = ('first_domain', 'domain', 'ip', 'update_date')
    search_fields = ['first_domain']


class AppTypeAdmin(object):
    list_display = ('domain', 'name', 'cata', 'implies', 'update_date')
    search_fields = ['domain']


class OpenPortAdmin(object):
    list_display = ('ip_addr', 'port_num', 'port_info', 'update_date')
    search_fields = ['ip_addr']


class DomainBruteAdmin(object):
    list_display = ('target_first_domain', 'target_domain', 'status', 'domain_count', 'current_index', 'thread', 'model', 'update_date')
    search_fields = ['target_first_domain']


class SpiderAdmin(object):
    list_display = ('target_domain', 'target_url', 'status', 'thread', 'update_date')
    search_fields = ['target_domain']


class WebProofAdmin(object):
    list_display = ('target_url', 'target_domain', 'status', 'update_date')
    search_fields = ['target_url']


class WebProofResultAdmin(object):
    list_display = ('domain', 'result', 'poc_type', 'poc_name', 'update_date')
    search_fields = ['domain']


class UploadPocAdmin(object):
    list_display = ('app_name', 'poc_name', 'poc_path')
    search_fields = ['app_name']
    # wizard_form_list = [('上传poc', ('app_name', 'poc_name', 'poc_path'))]
        # ('Frist\'s Form', ('name', 'description')),
        # ('Seocnd Form', ('contact', 'telphone', 'address')),
        # ('Thread Form', ('customer_id',))


# class MyUserAdmin(object):
#     # list_diaplsy = (
#     # 'user','port_scan_model', 'port_scan_thread', 'domain_brute_model', 'domain_brute_thread', 'spider_thread' 'single_web_attack', 'batch_web_attack', 'port_scan', 'domain_brute' 'spider', 'port_scan_model',
#     # 'port_scan_thread', 'domain_brute_model', 'domain_brute_thread', 'spider_thread')
#     search_fields = ['username']

class UserPowerAdmin(object):
    list_display = ('user', 'single_web_task', 'batch_web_task', 'port_scan', 'domain_brute', 'spider')
    search_fields = ['user']


class UserSettingAdmin(object):
    list_display = (
    'user', 'port_scan_model', 'port_scan_thread', 'domain_brute_model', 'domain_brute_thread', 'spider_thread')
    search_fields = ['user']


class AppTagAdmin(object):
    list_display = (
        'name', 'cata'
    )


class UploadPocAdmin(object):
    list_display = {
        'user', 'app_tag', 'app_version', 'poc_type', 'poc_name', 'poc_desc', 'poc_path', 'status', 'update_date'
    }


class IdentifyAdmin(AdminSite):
    site_header = 'xxx'


# xadmin.site.register(CommAdminView, GlobalSetting)


xadmin.site.register(WebSingleTask, WebSingleTaskAdmin)
xadmin.site.register(Finger, FingerAdmin)
xadmin.site.register(PortScan, PortScanAdmin)
xadmin.site.register(Url, UrlAdmin)
xadmin.site.register(DomainIP, DomainIpAdmin)
xadmin.site.register(AppType, AppTypeAdmin)
xadmin.site.register(OpenPort, OpenPortAdmin)
xadmin.site.register(DomainBrute, DomainBruteAdmin)
xadmin.site.register(Spider, SpiderAdmin)
xadmin.site.register(WebProof, WebProofAdmin)
xadmin.site.register(WebProofResult, WebProofResultAdmin)
# xadmin.site.register(UserSettings, UserSettingsAdmin)
# xadmin.site.register(UploadPoc, UploadPocAdmin)
# xadmin.site.register(User, UserAdmin)
xadmin.site.register(UserPower, UserPowerAdmin)
xadmin.site.register(UserSetting, UserSettingAdmin)
xadmin.site.register(AppTag, AppTagAdmin)
xadmin.site.register(UploadPoc, UploadPocAdmin)

# identify_admin = IdentifyAdmin(name='iudentify')
# identify_admin.register(IdentifyAdmin)