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

class IpAddr(models.Model):
    # id = models.IntegerField(max_length=32, auto_created=1, primary_key=True)
    ip = models.CharField(max_length=56)


class Domain(models.Model):
    # id = models.IntegerField(max_length=32, auto_created=1, primary_key=True)
    domain = models.CharField(max_length=128)
    level = models.IntegerField()       #二级，三级，四级域名，0为target目标域名
    ip = models.ManyToManyField(IpAddr, null=True)


class Url(models.Model):
    # id = models.IntegerField(max_length=32, auto_created=1, primary_key=True)
    url = models.CharField(max_length=256)


# 暂时无用
# class TargetInfo(models.Model):
#     # id = models.IntegerField(max_length=32, auto_created=1, primary_key=True)
#     domain = models.ForeignKey(Domain)
#     ip = models.ManyToManyField(IpAddr)


class SingleTask(models.Model):
    # id = models.IntegerField(max_length=32, auto_created=1, primary_key=True)
    # task_name = models.CharField(max_length=32)
    target_url = models.CharField(max_length=32, null=False)            #目标网址
    task_status = models.SmallIntegerField(default=0)          #任务完成状态，1完成，0未完成
    task_rate = models.IntegerField(default=0)            #任务进度百分比


class BatchTask(models.Model):
    # id = models.IntegerField(max_length=32, auto_created=1, primary_key=True)
    # task_name = models.CharField(max_length=32)
    target_domain = models.ManyToManyField(Domain)
    task_status = models.SmallIntegerField(default=0)
    task_rate = models.IntegerField(default=0)
    domain_num = models.IntegerField(default=0)
    complete_num = models.IntegerField(default=0)


class Finger(models.Model):
    # id = models.IntegerField(max_length=32, auto_created=1, primary_key=True)
    task_id = models.ForeignKey(SingleTask)
    task_type = models.IntegerField(default=0)          # 0为单个任务，1为批量任务
    target = models.CharField(max_length=32)
    finger_status = models.SmallIntegerField(default=0)
    finger_rate = models.IntegerField(default=0)
    # 指纹结果，暂时使用json存取所有，后期分猜为多个字段
    # 指纹对应json和cata后期可存放于数据库
    finger_result_json = models.CharField(max_length=256, null=True)


class PortScan(models.Model):
    # id = models.IntegerField(max_length=32, auto_created=1, primary_key=True)
    # target_domain = models.CharField(max_length=32)
    target_ip = models.CharField(max_length=32)
    task_id = models.ForeignKey(SingleTask)
    task_type = models.IntegerField(default=0)  # 0为单个任务，1为批量任务
    port_scan_status = models.SmallIntegerField(default=0)
    port_scan_rate = models.IntegerField(default=0)
    port_scan_thread = models.IntegerField(default=4)
    port_scan_model = models.CharField(max_length=16, default='usually')
    # 扫描结果每个端口对应信息，后期可存放于数据库。目前使用json数据存取结果。
    port_scan_result_json = models.CharField(max_length=512, null=True)


class DomainBrute(models.Model):
    # id = models.IntegerField(max_length=32, auto_created=1, primary_key=True)
    task_id = models.ForeignKey(SingleTask)
    task_type = models.IntegerField(default=0)  # 0为单个任务，1为批量任务
    target_domain = models.CharField(max_length=32)
    domain_brute_status = models.SmallIntegerField(default=0)
    domain_brute_rate = models.IntegerField(default=0)
    domain_brute_thread = models.IntegerField(default=4)
    # domain_brute_rate，后期可以增加多个模式，分为二级域名爆破及递归爆破子域名。
    domain_brute_result_json = models.CharField(max_length=512, null=True)     #后期可将所有子域名分别存为domain表中


class Spider(models.Model):
    # id = models.IntegerField(max_length=32, auto_created=1, primary_key=True)
    task_id = models.ForeignKey(SingleTask)
    task_type = models.IntegerField(default=0)  # 0为单个任务，1为批量任务
    target_domain = models.CharField(max_length=32)
    spider_status = models.SmallIntegerField(default=0)
    spider_rate = models.IntegerField(default=0)
    spider_thread = models.IntegerField(default=4)
    # spider_result = models.ManyToManyField(Url, null=True)
    spider_result_json = models.TextField(max_length=102400, null=True)      #改为分别存放url


class ExploitAttack(models.Model):
    task_id = models.ForeignKey(SingleTask)
    task_type = models.IntegerField(default=0)  # 0为单个任务，1为批量任务
    target_domain = models.CharField(max_length=32)
    exploit_attack_status = models.SmallIntegerField(default=0)
    exploit_attack_rate = models.IntegerField(default=0)
    # exploit_attack_thread =
    exploit_attack_result_json = models.CharField(max_length=256, null=True)   #后期可改为每个漏洞分表