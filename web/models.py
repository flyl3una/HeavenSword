#env/bin/python
#coding:utf-8

from __future__ import unicode_literals

import os
import shutil

from django.contrib.auth.models import User, AbstractUser
from django.db import models
# Create your models here.


# class SwordUser(models.Model):
#     id = models.IntegerField(max_length=32, auto_created=1, primary_key=True)
#     username = models.CharField(max_length=32)
#     password = models.CharField(max_length=20)
#     email = models.EmailField(max_length=32)
#     mobile = models.IntegerField(max_length=12)
#
#     status = models.IntegerField(max_length=1)
#
#     class Mete:
#         def __init__(self):
#             pass
#         unique_together = (("user", "status"),)
#
#     def __unicode__(self):
#         return self.user.username
from HeavenSword.settings import TOOLS_PATH, UPLOAD_PATH
from tools.config import POC_PATH


class DomainIP(models.Model):
    first_domain = models.CharField(max_length=64, verbose_name='一级域名')
    domain = models.CharField(max_length=128, verbose_name='域名')
    ip = models.CharField(max_length=56, verbose_name='ip地址')
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return '域名对应ip信息'

    class Meta:
        verbose_name = '域名对应ip信息'
        verbose_name_plural = '域名对应ip信息'
# class IpAddr(models.Model):
    # ip = models.CharField(max_length=56, unique=True)
    # update_date = models.DateTimeField(auto_now=True)

# class Domain(models.Model):
#     domain = models.CharField(max_length=128, unique=True)
#     level = models.IntegerField()       #二级，三级，四级域名，0为target目标域名
#     ip = models.ManyToManyField(IpAddr, null=True)
#     update_date = models.DateTimeField(auto_now=True)


class Url(models.Model):
    # id = models.IntegerField(max_length=32, auto_created=1, primary_key=True)
    domain = models.CharField(max_length=128, verbose_name='域名')
    url = models.CharField(max_length=256, verbose_name='url地址')
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return 'url信息'

    class Meta:
        verbose_name = 'url信息'
        verbose_name_plural = 'url信息'

# 暂时无用
# class TargetInfo(models.Model):
#     # id = models.IntegerField(max_length=32, auto_created=1, primary_key=True)
#     domain = models.ForeignKey(Domain)
#     ip = models.ManyToManyField(IpAddr)


# class SingleTask(models.Model):
    # target_url = models.CharField(max_length=32, null=False)            #目标网址
    # status = models.SmallIntegerField(default=0)          #任务完成状态，1完成，0未完成
    # # 关联各个扫描任务
    # finger_id = models.IntegerField(default=0)
    # port_scan_ids = models.CharField(max_length=128)
    # spider_id = models.IntegerField(default=0)
    # domain_brute_id = models.IntegerField(default=0)
    # exploit_id = models.IntegerField(default=0)
    # update_date = models.DateTimeField(auto_now=True)


class WebSingleTask(models.Model):
    target_url = models.CharField(max_length=32, null=False, verbose_name='目标网址')  # 目标网址
    domain = models.CharField(max_length=32, unique=True, null=False, verbose_name='域名')    #目标域名
    status = models.SmallIntegerField(default=0, verbose_name='任务完成状态')  # 任务完成状态，1完成，0未完成
    finger_id = models.IntegerField(default=0, verbose_name='指纹识别表id')
    proof_id = models.IntegerField(default=0, verbose_name='exp利用表id')
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return '单一web任务'

    class Meta:
        verbose_name = '单一web任务'
        verbose_name_plural = '单一web任务'

# class AutoTask(models.Model):
#     target_url = models.CharField(max_length=32, null=False)  # 目标网址
#     status = models.SmallIntegerField(default=0)  # 任务完成状态，1完成，0未完成
#     update_date = models.DateTimeField(auto_now=True)

# class BatchTask(models.Model):
    # task_name = models.CharField(max_length=32)
    # target_domain = models.ManyToManyField(Domain)
    # task_status = models.SmallIntegerField(default=0)
    # task_rate = models.IntegerField(default=0)
    # domain_num = models.IntegerField(default=0)
    # complete_num = models.IntegerField(default=0)
    # update_date = models.DateTimeField(auto_now=True)


class AppType(models.Model):
    domain = models.CharField(max_length=128, verbose_name='域名')
    name = models.CharField(max_length=32, verbose_name='app名称')
    cata = models.CharField(max_length=32, verbose_name='app类型')
    implies = models.CharField(max_length=32, verbose_name='app额外信息', null=True)
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return 'web app结果'

    class Meta:
        verbose_name = 'web app结果'
        verbose_name_plural = 'web app结果'


class OpenPort(models.Model):
    ip_addr = models.CharField(max_length=32, null=False, verbose_name='ip地址')
    port_num = models.IntegerField(null=False, verbose_name='端口号')
    port_info = models.CharField(max_length=512, verbose_name='端口信息')
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return '端口开放信息'

    class Meta:
        verbose_name = '端口开放信息'
        verbose_name_plural = '端口开放信息'


class Finger(models.Model):
    # id = models.IntegerField(max_length=32, auto_created=1, primary_key=True)
    # task_id = models.ForeignKey(SingleTask)
    # task_type = models.IntegerField(default=0)          # 0为单个任务，1为批量任务
    target_domain = models.CharField(max_length=32, unique=True, verbose_name='目标域名')
    target_url = models.CharField(max_length=128, unique=True, verbose_name='目标url地址')
    # 31,request请求目标地址错误。
    status = models.SmallIntegerField(default=0, verbose_name='指纹识别任务状态')     # 0未开始，1开始，2完成, 3xxx异常出错
    # finger_rate = models.IntegerField(default=0)
    finger_count = models.IntegerField(default=3000, verbose_name='待测试指纹总数')        #所有待指纹类型
    current_index = models.IntegerField(default=0, verbose_name='当前指纹匹配位置')          #当前匹配指纹位置
    # 指纹结果，暂时使用json存取所有，后期分猜为多个字段
    # 指纹对应json和cata后期可存放于数据库
    # finger_result_json = models.CharField(max_length=1024, null=True)
    # 为了防止删除该任务时把域名和ip的对应信息删除，特不做关联，直接根据一级域名查询apptype表即可。
    # finger_result = models.ManyToManyField(AppType, null=True)
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return '指纹识别任务'

    class Meta:
        verbose_name = '指纹识别任务'
        verbose_name_plural = '指纹识别任务'


# 用户使用过的工具
# class UserTools(models.Model):
#     user = models.ForeignKey(User)
#     port_scan = models.ForeignKey(PortScan)
#     spider = models.ForeignKey(Spider)
#     domain_brute = models.ForeignKey(domain_brute)


class PortScan(models.Model):
    # id = models.IntegerField(max_length=32, auto_created=1, primary_key=True)
    # target_domain = models.CharField(max_length=32)
    target_ip = models.CharField(max_length=32, unique=True, verbose_name='目标ip地址')
    # task_id = models.ForeignKey(SingleTask)
    # task_type = models.IntegerField(default=0)  # 0为单个任务，1为批量任务
    status = models.SmallIntegerField(default=0, verbose_name='端口扫描任务状态')
    # port_scan_rate = models.IntegerField(default=0)
    port_count = models.IntegerField(default=53325, verbose_name='待扫描端口数')         # 所有待端口个数
    current_index = models.IntegerField(default=0, verbose_name='当前端口扫描索引')          # 当前扫描端口索引
    thread = models.IntegerField(default=4, verbose_name='端口扫描线程')
    model = models.CharField(max_length=16, default='usually', verbose_name='端口扫描模式')
    # 扫描结果每个端口对应信息，后期可存放于数据库。目前使用json数据存取结果。
    # port_scan_result_json = models.CharField(max_length=512, null=True)
    # 为了防止删除该任务时把域名和ip的对应信息删除，特不做关联，直接根据一级域名查询openport表即可。
    # port_scan_result = models.ManyToManyField(OpenPort, null=True)
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return '端口扫描任务'

    class Meta:
        verbose_name = '端口扫描任务'
        verbose_name_plural = '端口扫描任务'


class DomainBrute(models.Model):
    # id = models.IntegerField(max_length=32, auto_created=1, primary_key=True)
    # task_id = models.ForeignKey(SingleTask)
    # task_type = models.IntegerField(default=0)  # 0为单个任务，1为批量任务
    target_first_domain = models.CharField(max_length=32, unique=True, verbose_name='目标父域名')
    target_domain = models.CharField(max_length=32, unique=True, verbose_name='目标域名')
    status = models.SmallIntegerField(default=0, verbose_name='任务状态')
    # domain_brute_rate = models.IntegerField(default=0)
    domain_count = models.IntegerField(default=10000, verbose_name='待爆破域名数')       # 所有待爆破域名数
    current_index = models.IntegerField(default=0, verbose_name='当前爆破域名索引')          # 当前端口爆破索引
    thread = models.IntegerField(default=4, verbose_name='域名爆破线程')
    model = models.CharField(max_length=16, default='usually', verbose_name='爆破类型')
    # domain_brute_rate，后期可以增加多个模式，分为二级域名爆破及递归爆破子域名。
    # domain_brute_result_json = models.CharField(max_length=512, null=True)     #后期可将所有子域名分别存为domain表中
    # 为了防止删除该任务时把域名和ip的对应信息删除，特不做关联，直接根据一级域名查询domain表即可。
    # domain_result = models.ManyToManyField(Domain)
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return '域名爆破任务'

    class Meta:
        verbose_name = '域名爆破任务'
        verbose_name_plural = '域名爆破任务'


class Spider(models.Model):
    # id = models.IntegerField(max_length=32, auto_created=1, primary_key=True)
    # task_id = models.ForeignKey(SingleTask)
    # task_type = models.IntegerField(default=0)  # 0为单个任务，1为批量任务
    target_domain = models.CharField(max_length=32, unique=True, verbose_name='目标域名')
    target_url = models.CharField(max_length=128, default=None, verbose_name='目标url地址')
    status = models.SmallIntegerField(default=0, verbose_name='web爬虫状态')
    # all_url = models.IntegerField(default=1)        # 当前爬取到的链接总数
    # spider_rate = models.IntegerField(default=0)
    thread = models.IntegerField(default=4, verbose_name='web爬虫线程')
    # spider_result = models.ManyToManyField(Url, null=True)
    # spider_result_json = models.TextField(max_length=102400, null=True)      #改为分别存放url
    # 为了防止删除该任务时把域名和ip的对应信息删除，特不做关联，直接根据域名查询url表即可。
    # spider_result = models.ManyToManyField(Url)
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return 'web爬虫任务'

    class Meta:
        verbose_name = 'web爬虫任务'
        verbose_name_plural = 'web爬虫任务'


class UserTaskId(models.Model):
    user = models.ForeignKey(User, verbose_name='用户id')
    task = models.ForeignKey(WebSingleTask, verbose_name='任务id')

    def __str__(self):
        return '用户任务列表'

    class Meta:
        verbose_name = '用户任务列表'
        verbose_name_plural = '用户任务列表'


class WebProof(models.Model):
    # task_id = models.ForeignKey(SingleTask)
    # task_type = models.IntegerField(default=0)  # 0为单个任务，1为批量任务
    target_url = models.CharField(max_length=128, unique=True, verbose_name='目标域名')
    target_domain = models.CharField(max_length=32, verbose_name='目标域名')
    status = models.SmallIntegerField(default=0, verbose_name='exp测试状态')
    poc_count = models.IntegerField(default=10, verbose_name='该app的exp数量')         # 该指纹的所有exp个数
    current_index = models.IntegerField(default=0, verbose_name='当前匹配索引')          # 当前匹配指纹索引
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return 'web exp测试'

    class Meta:
        verbose_name = 'web exp测试'
        verbose_name_plural = 'web exp测试'


class WebProofResult(models.Model):
    domain = models.CharField(max_length=32, verbose_name='目标域名')
    result = models.IntegerField(default=0, verbose_name='结果')         # 0表示没有漏洞，1表示exp攻击成功
    poc_type = models.CharField(max_length=32, verbose_name='exp类型')      # exp类型
    poc_name = models.CharField(max_length=32, verbose_name='exp名称')      # 成功使用的exp名称
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return 'web exp利用结果'

    class Meta:
        verbose_name = 'web exp利用结果'
        verbose_name_plural = 'web exp利用结果'


class AppTag(models.Model):
    name = models.CharField(max_length=32, null=None, verbose_name='app名称')
    cata = models.CharField(max_length=64, null=None, verbose_name='app类型')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'web app类型'
        verbose_name_plural = 'web app类型'


class UploadPoc(models.Model):
    user = models.ForeignKey(User, verbose_name='上传用户id')
    app_tag = models.ForeignKey(AppTag, verbose_name='app类型')
    app_version = models.CharField(max_length=32, null=True, default=" ", verbose_name='app版本信息')
    poc_type = models.CharField(max_length=32, default='web', verbose_name='poc类型')
    poc_name = models.CharField(max_length=32, verbose_name='poc名称')
    poc_desc = models.CharField(max_length=128, verbose_name='描述')
    poc_path = models.CharField(max_length=128, verbose_name='文件名称')
    # poc_file = models.FileField(upload_to=UPLOAD_PATH, null=None, verbose_name='上传路径')
    file_content = models.TextField(verbose_name='poc脚本内容')
    status = models.BooleanField(default=False, verbose_name='poc审查状态')
    update_date = models.DateTimeField(auto_now=True, verbose_name='上传时间')

    def __str__(self):
        return 'poc上传'

    # def get_file_content(self):
    #     # file_content = self.poc_file.read()
    #     file_content = file(self.poc_file).read()
    #     return file_content

    class Meta:

        verbose_name = 'poc上传'
        verbose_name_plural = 'poc上传'

    def __move_file(self):
        try:
            tmp_path = os.path.join(UPLOAD_PATH, self.poc_path)
            real_path = os.path.join(POC_PATH, self.poc_type, self.app_tag.name, self.poc_path)
            if self.status:
                if os.path.exists(tmp_path) and not os.path.exists(real_path):
                    if not os.path.exists(os.path.join(POC_PATH, self.poc_type, self.app_tag.name)):
                        os.mkdir(os.path.join(POC_PATH, self.poc_type, self.app_tag.name))
                    shutil.move(tmp_path, real_path)
            else:
                if os.path.exists(tmp_path) and not os.path.exists(real_path):
                    pass
                elif os.path.exists(real_path) and not os.path.exists(tmp_path):
                    shutil.move(real_path, tmp_path)
        except Exception as e:
            print '保存文件时文件移动错误'
            print e

    def __delete_file(self):
        try:
            tmp_path = os.path.join(UPLOAD_PATH, self.poc_path)
            real_path = os.path.join(POC_PATH, self.poc_type, self.app_tag.name, self.poc_path)
            if self.status:
                os.remove(real_path)
            else:
                os.remove(tmp_path)
        except Exception as e:
            print '删除文件时文件移动错误'
            print e

    # 移动文件重写save和delete函数
    def save(self):
        self.__move_file()
        super(UploadPoc, self).save()

    def delete(self, using=None, keep_parents=False):
        print 'delete'
        self.__delete_file()
        super(UploadPoc, self).delete(using=None, keep_parents=False)


class UserPower(models.Model):
    user = models.ForeignKey(User, verbose_name='用户')
    single_web_task = models.BooleanField(default=True, verbose_name='web检测权限')
    batch_web_task = models.BooleanField(default=True, verbose_name='web批量检测权限')
    port_scan = models.BooleanField(default=True, verbose_name='端口扫描权限')
    domain_brute = models.BooleanField(default=True, verbose_name='域名爆破权限')
    spider = models.BooleanField(default=True, verbose_name='web爬虫权限')
    # update_date = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return '用户权限'

    class Meta:
        verbose_name = '用户权限'
        verbose_name_plural = '用户权限'


class UserSetting(models.Model):
    user = models.ForeignKey(User, verbose_name='用户')
    port_scan_model = models.CharField(max_length=32, null=None, default='usually', verbose_name='端口扫描模式')
    port_scan_thread = models.IntegerField(default=4, null=None, verbose_name='端口扫描线程')
    domain_brute_model = models.CharField(max_length=32, null=None, default='usually', verbose_name='域名爆破模式')
    domain_brute_thread = models.IntegerField(default=4, null=None, verbose_name='域名爆破线程')
    spider_thread = models.IntegerField(default=4, null=None, verbose_name='web爬虫线程')
    # update_date = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return '用户配置'

    class Meta:
        verbose_name = '用户配置'
        verbose_name_plural = '用户配置'
