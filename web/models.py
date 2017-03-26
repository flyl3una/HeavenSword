#env/bin/python
#coding:utf-8

from __future__ import unicode_literals

from django.contrib.auth.models import User
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

class DomainIP(models.Model):
    first_domain = models.CharField(max_length=64)
    domain = models.CharField(max_length=128)
    ip = models.CharField(max_length=56)
    update_date = models.DateTimeField(auto_now=True)


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
    domain = models.CharField(max_length=128)
    url = models.CharField(max_length=256)
    update_date = models.DateTimeField(auto_now=True)


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
    target_url = models.CharField(max_length=32, null=False)  # 目标网址
    domain = models.CharField(max_length=32, unique=True, null=False)    #目标域名
    status = models.SmallIntegerField(default=0)  # 任务完成状态，1完成，0未完成
    finger_id = models.IntegerField(default=0)
    exploit_id = models.IntegerField(default=0)
    update_date = models.DateTimeField(auto_now=True)


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
    domain = models.CharField(max_length=128)
    name = models.CharField(max_length=32)
    cata = models.CharField(max_length=32)
    implies = models.CharField(max_length=32)
    # update_date = models.DateTimeField


class OpenPort(models.Model):
    ip_addr = models.CharField(max_length=32, null=False)
    port_num = models.IntegerField(null=False)
    port_info = models.CharField(max_length=512)


class Finger(models.Model):
    # id = models.IntegerField(max_length=32, auto_created=1, primary_key=True)
    # task_id = models.ForeignKey(SingleTask)
    # task_type = models.IntegerField(default=0)          # 0为单个任务，1为批量任务
    target_domain = models.CharField(max_length=32, unique=True)
    target_url = models.CharField(max_length=128, unique=True)
    # 31,request请求目标地址错误。
    status = models.SmallIntegerField(default=0)     # 0未开始，1开始，2完成, 3xxx异常出错
    # finger_rate = models.IntegerField(default=0)
    finger_count = models.IntegerField(default=3000)        #所有待指纹类型
    current_index = models.IntegerField(default=0)          #当前匹配指纹位置
    # 指纹结果，暂时使用json存取所有，后期分猜为多个字段
    # 指纹对应json和cata后期可存放于数据库
    # finger_result_json = models.CharField(max_length=1024, null=True)
    # 为了防止删除该任务时把域名和ip的对应信息删除，特不做关联，直接根据一级域名查询apptype表即可。
    # finger_result = models.ManyToManyField(AppType, null=True)
    update_date = models.DateTimeField(auto_now=True)


# 用户使用过的工具
# class UserTools(models.Model):
#     user = models.ForeignKey(User)
#     port_scan = models.ForeignKey(PortScan)
#     spider = models.ForeignKey(Spider)
#     domain_brute = models.ForeignKey(domain_brute)


class PortScan(models.Model):
    # id = models.IntegerField(max_length=32, auto_created=1, primary_key=True)
    # target_domain = models.CharField(max_length=32)
    target_ip = models.CharField(max_length=32, unique=True)
    # task_id = models.ForeignKey(SingleTask)
    # task_type = models.IntegerField(default=0)  # 0为单个任务，1为批量任务
    status = models.SmallIntegerField(default=0)
    # port_scan_rate = models.IntegerField(default=0)
    port_count = models.IntegerField(default=53325)         # 所有待端口个数
    current_index = models.IntegerField(default=0)          # 当前扫描端口索引
    thread = models.IntegerField(default=4)
    model = models.CharField(max_length=16, default='usually')
    # 扫描结果每个端口对应信息，后期可存放于数据库。目前使用json数据存取结果。
    # port_scan_result_json = models.CharField(max_length=512, null=True)
    # 为了防止删除该任务时把域名和ip的对应信息删除，特不做关联，直接根据一级域名查询openport表即可。
    # port_scan_result = models.ManyToManyField(OpenPort, null=True)
    update_date = models.DateTimeField(auto_now=True)


class DomainBrute(models.Model):
    # id = models.IntegerField(max_length=32, auto_created=1, primary_key=True)
    # task_id = models.ForeignKey(SingleTask)
    # task_type = models.IntegerField(default=0)  # 0为单个任务，1为批量任务
    target_first_domain = models.CharField(max_length=32, unique=True)
    target_domain = models.CharField(max_length=32, unique=True)
    status = models.SmallIntegerField(default=0)
    # domain_brute_rate = models.IntegerField(default=0)
    domain_count = models.IntegerField(default=10000)       # 所有待爆破域名数
    current_index = models.IntegerField(default=0)          # 当前端口爆破索引
    thread = models.IntegerField(default=4)
    model = models.CharField(max_length=16, default='usually')
    # domain_brute_rate，后期可以增加多个模式，分为二级域名爆破及递归爆破子域名。
    # domain_brute_result_json = models.CharField(max_length=512, null=True)     #后期可将所有子域名分别存为domain表中
    # 为了防止删除该任务时把域名和ip的对应信息删除，特不做关联，直接根据一级域名查询domain表即可。
    # domain_result = models.ManyToManyField(Domain)
    update_date = models.DateTimeField(auto_now=True)


class Spider(models.Model):
    # id = models.IntegerField(max_length=32, auto_created=1, primary_key=True)
    # task_id = models.ForeignKey(SingleTask)
    # task_type = models.IntegerField(default=0)  # 0为单个任务，1为批量任务
    target_domain = models.CharField(max_length=32, unique=True)
    target_url = models.CharField(max_length=128, default=None)
    status = models.SmallIntegerField(default=0)
    # all_url = models.IntegerField(default=1)        # 当前爬取到的链接总数
    # spider_rate = models.IntegerField(default=0)
    thread = models.IntegerField(default=4)
    # spider_result = models.ManyToManyField(Url, null=True)
    # spider_result_json = models.TextField(max_length=102400, null=True)      #改为分别存放url
    # 为了防止删除该任务时把域名和ip的对应信息删除，特不做关联，直接根据域名查询url表即可。
    # spider_result = models.ManyToManyField(Url)
    update_date = models.DateTimeField(auto_now=True)


class WebExploit(models.Model):
    # task_id = models.ForeignKey(SingleTask)
    # task_type = models.IntegerField(default=0)  # 0为单个任务，1为批量任务
    target_url = models.CharField(max_length=128, unique=True)
    target_domain = models.CharField(max_length=32)
    status = models.SmallIntegerField(default=0)
    exp_count = models.IntegerField(default=10)         # 该指纹的所有exp个数
    current_index = models.IntegerField(default=0)          # 当前匹配指纹索引
    # exploit_result = models.IntegerField(default=0)         # 0表示没有漏洞，1表示exp攻击成功
    # exploit_exp_type = models.CharField(max_length=32)      # 漏洞利用成功后
    # exploit_attack_rate = models.IntegerField(default=0)
    # exploit_attack_thread =
    # exploit_attack_result_json = models.CharField(max_length=256, null=True)   #后期可改为每个漏洞分表
    update_date = models.DateTimeField(auto_now=True)


class WebExploitResult(models.Model):
    domain = models.CharField(max_length=32)
    result = models.IntegerField(default=0)         # 0表示没有漏洞，1表示exp攻击成功
    exp_type = models.CharField(max_length=32)      # exp类型
    exp_name = models.CharField(max_length=32)      # 成功使用的exp名称