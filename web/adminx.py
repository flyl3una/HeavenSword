# coding=utf-8
import xadmin
from django.contrib import admin
from django.contrib.admin.utils import get_deleted_objects
from django.core.exceptions import PermissionDenied
from django.db import router
from django.template.response import TemplateResponse
from django.utils.encoding import force_unicode
from xadmin import AdminSite, widgets
from xadmin.plugins.actions import BaseActionView, DeleteSelectedAction, ACTION_CHECKBOX_NAME
from xadmin.util import model_ngettext
from xadmin.views import filter_hook

from web.models import *



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


def IdentifyPassAction(BaseActionView):
    print 'ss'
    pass


class DeletePocFileAction(BaseActionView):
    action_name = "delete_selected"
    description = u'Delete POC File %(verbose_name_plural)s'

    delete_confirmation_template = None
    delete_selected_confirmation_template = None

    delete_models_batch = True

    model_perm = 'delete'
    icon = 'fa fa-times'

    # @filter_hook
    def delete_models(self, queryset):
        n = queryset.count()
        if n:
            for obj in queryset:
                obj.delete()
            self.message_user("Successfully deleted %(count)d %(items)s." % {
                "count": n, "items": model_ngettext(self.opts, n)
            }, 'success')

    # @filter_hook
    def do_action(self, queryset):
        # Check that the user has delete permission for the actual model
        if not self.has_delete_permission():
            raise PermissionDenied

        using = router.db_for_write(self.model)

        # Populate deletable_objects, a data structure of all related objects that
        # will also be deleted.
        deletable_objects, model_count, perms_needed, protected = get_deleted_objects(
            queryset, self.opts, self.user, self.admin_site, using)

        # The user has already confirmed the deletion.
        # Do the deletion and return a None to display the change list view again.
        if self.request.POST.get('post'):
            if perms_needed:
                raise PermissionDenied
            self.delete_models(queryset)
            # Return None to display the change list page again.
            return None

        if len(queryset) == 1:
            objects_name = force_unicode(self.opts.verbose_name)
        else:
            objects_name = force_unicode(self.opts.verbose_name_plural)

        if perms_needed or protected:
            title = "Cannot delete %(name)s" % {"name": objects_name}
        else:
            title = "Are you sure?"

        context = self.get_context()
        context.update({
            "title": title,
            "objects_name": objects_name,
            "deletable_objects": [deletable_objects],
            'queryset': queryset,
            "perms_lacking": perms_needed,
            "protected": protected,
            "opts": self.opts,
            "app_label": self.app_label,
            'action_checkbox_name': ACTION_CHECKBOX_NAME,
        })

        # Display the confirmation page
        return TemplateResponse(self.request, self.delete_selected_confirmation_template or
                                self.get_template_list('views/model_delete_selected_confirm.html'), context,
                                current_app=self.admin_site.name)


class UploadPocAdmin(object):
    list_display = {
        'user', 'app_tag', 'app_version', 'poc_type', 'poc_name', 'poc_desc', 'status', 'update_date'
    }
    search_fields = ['app_tag']
    list_display_links = ('status', )
    # list_editable = ('user', 'app_tag', 'app_version', 'poc_type', 'poc_desc', 'status')
    # file_display = ('poc_path', )

    formfield_overrides = {
        models.FileField: {'widget': widgets.AdminFileWidget},
    }

    # 自定义批量操作的action
    # def delete_file_action(modelxadmin, request, queryset):
    #     # queryset.update(status='p')
    #     print 'xx'
    #     pass
    # delete_file_action.short_description = "aa"

    actions = [DeletePocFileAction, ]

    # def file_content(self, obj):
    #     return obj.poc_file.read()
    # file_content.poc_file = 'UploadPoc'


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