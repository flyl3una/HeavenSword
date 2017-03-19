# coding=utf-8
import json
import os
import socket
import subprocess

import time
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from HeavenSword.settings import DEFAULT_FROM_EMAIL, EMAIL_HOST_USER, CORE_PATH
from core.function import get_ip, get_domain, get_first_domain, get_root_url
from web import models
from web.dir.EmailToken import EmailToken
from web.models import WebSingleTask
from web.msetting import DOMAIN


def index(request):
    username = ''
    if request.method == 'GET':
        if request.user.is_authenticated():
            username = request.COOKIES.get("username")
        return render(request, 'index.html', {'username': username})
    if request.method == 'POST':
        url = request.POST.get('target')
        # print url
        return render(request, 'index.html', {'username': username})


def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
        # return HttpResponse("""您已经登陆!<br/><a href="/index/">点击跳转到主页</a>""")
    if request.method == 'GET':
        return render(request, 'login1.html')
    if request.method == 'POST':
        # username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = User.objects.get(email=email).get_username()
        user = authenticate(username=username, password=password)
        # print email, password
        if user:
            if user.is_active:
                login(request, user)
                response = HttpResponseRedirect('/')

                response.set_cookie('username', username, max_age=None)
                # return redirect(reverse('views.index'), args=[])
                return response
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(email, password)
            return HttpResponse("Invalid login details supplied.")


def user_logout(request):
    logout(request)
    # return render(request, '/')
    return HttpResponseRedirect('/')


def user_register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        params = request.POST
        email = params['email']
        password = params['password']
        password2 = params['password2']
        username = params['username']
        try:
            user = User.objects.get(username=username)
            return HttpResponse("<script>parent.register_has_user();</script>")
        except:
            pass
        try:
            user = User.objects.get(email=email)
            return HttpResponse("<script>parent.register_has_email();</script>")
        except:
            if password is None or password2 is None:
                return HttpResponse("<script>parent.register_error2();</script>")
            if password != password2:
                return HttpResponse("<script>parent.register_error1();</script>")
        user = User(username=username, email=email)
        user.set_password(password)
        user.is_active = False

        token_confirm = EmailToken('xqlpniip)kgj&dod5e=k95!q6su!m$tsy__&li3-vx)tflp#yr')
        token = token_confirm.generate_validate_token(username)
        # active_key = base64.encodestring(username)
        # send email to the register email
        message = "\n".join([
            u'{0},欢迎使用倚天剑'.format(username),
            u'请访问该链接，完成用户验证:',
            '/'.join([DOMAIN, 'user/activate', token])
        ])
        from_email = EMAIL_HOST_USER
        send_mail(u'注册用户验证信息', message, from_email, [email])
        user.save()
        return HttpResponse('<script>parent.register_success();</script>')
        # return HttpResponse("<script>parent.register_success();</script>")


def user_activate(request, token):
    token_confirm = EmailToken('xqlpniip)kgj&dod5e=k95!q6su!m$tsy__&li3-vx)tflp#yr')
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        return HttpResponse("连接已超时，请重新注册。")
    user = User.objects.get(username=username)
    user.is_active = True
    user.save()
    return HttpResponse("账号激活成功。<br><a href='/user/login/'>点击跳转到登陆页面</a>")


def about(request):
    return render(request, 'help.html')


def batch(request):
    return render(request, 'batch.html')


def operation(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            username = request.COOKIES.get("username")
            return render(request, 'operation.html', {'username': username})
    return HttpResponse("<div style='text-align:center;margin-top:20%'><h3>请登录</h3><br><br><a href='/user/login/'>点击跳转到登陆页面</a>")


def new_single_web_task1(request):
    if not request.user.is_authenticated():
        return HttpResponse("<div style='text-align:center;margin-top:20%'><h3>请登录</h3><br><br><a href='/user/login/'>点击跳转到登陆页面</a>")
    if request.method == 'GET':
        return render(request, 'task/new_single_task.html')
    if request.method == 'POST':
        params = request.POST
        try:
            if 'target' not in params:
                return HttpResponse("目标错误")
            args = {}
            target = params['target']
            target = get_root_url(target)
            args['target'] = target
            domain = get_domain(target)
            first_domain = get_first_domain(domain)
            ipaddrs = []
            try:
                ipaddrs = get_ip(domain)
            except Exception as e:
                print e
            ips = models.DomainIP.objects.filter(domain=domain).values('ip')
            for ip in ips:
                if ip['ip'] not in ipaddrs:
                    m_domainip = models.DomainIP(first_domain=first_domain, domain=domain, ip=ip)
                    m_domainip.save()

            m_single_task = models.SingleTask(target_url=target)
            m_single_task.save()
            # args['task_id'] = m_single_task.id

            if 'finger_flag' in params.keys():
                # 判断数据库是否已经有该域名的指纹识别了，如果有，则不在进行识别.后续加上对任务的判断，防止多个用户同时执行针对同一个目标的测试。
                # b_apptypes = models.AppType.objects.filter(domain=domain)
                b_finger = models.Finger.objects.filter(target_domain=domain)
                # b_finger_task = models.Finger.objects.filter()
                if b_finger:
                    args['finger_flag'] = False
                else:
                    args['finger_flag'] = True
                    m_finger = models.Finger(target_domain=domain, target_url=target)
                    m_finger.save()
                    args['finger_id'] = m_finger.id
                    args['finger_target_url'] = target
                    m_single_task.finger_id = m_finger.id
                # finger_ret = get_finger(target)
                # print finger_ret

            if 'port_scan_flag' in params.keys():
                # ip_addr = socket.gethostbyname(target)
                addrs = []
                for ip in ipaddrs:
                    b_port = models.PortScan.objects.filter(target_ip=ip)
                    # m_ports = models.OpenPort.objects.filter(ip_addr=ip)
                    if not b_port:
                        addrs.append(ip)
                if addrs:
                    args['port_scan_flag'] = True
                    args['port_addr2id'] = {}
                    ids = []
                    for ip in addrs:
                        m_port_scan = models.PortScan(target_ip=ip)
                        if 'port_scan_thread' in params.keys():
                            m_port_scan.port_scan_thread = params['port_scan_thread']
                            args['port_scan_thread'] = int(params['port_scan_thread'])
                        if 'port_scan_model' in params.keys():
                            m_port_scan.port_scan_model = params['port_scan_model']
                            args['port_scan_model'] = params['port_scan_model']
                        m_port_scan.save()
                        port_scan_id = int(m_port_scan.id)
                        ids.append(str(port_scan_id))
                        args['port_addr2id'][ip] = port_scan_id
                    args['port_addrs'] = addrs
                    m_single_task.port_scan_ids = '|'.join(ids)     #多个id用|分隔
                else:
                    args['port_scan_flag'] = False

                # new_port_scan(ip='113.105.245.122', model=str(params['port_scan_model']),
                #               thread_num=params['port_scan_thread'])
            if 'domain_brute_flag' in params.keys():
                # b_domain = models.DomainIP.objects.filter(first_domain=first_domain)
                b_domain = models.DomainBrute.objects.filter(target_first_domain=first_domain)
                if not b_domain:
                    m_domain_brute = models.DomainBrute(target_first_domain=first_domain, target_domain=domain)
                    args['domain_brute_flag'] = True
                    args['target_first_domain'] = first_domain
                    if 'domain_brute_thread' in params.keys():
                        m_domain_brute.domain_brute_thread = params['domain_brute_thread']
                        args['domain_brute_thread'] = int(params['domain_brute_thread'])
                        # domain_brute_thread_num = params['domain_brute_thread']
                        # new_domain_brute('runboo.com', domain_brute_thread_num)
                    m_domain_brute.save()
                    args['domain_brute_id'] = m_domain_brute.id
                    m_single_task.domain_brute_id = m_domain_brute.id
                else:
                    args['domain_brute_flag'] = False

            if 'spider_flag' in params.keys():
                # b_spider = models.Url.objects.filter(domain=domain)
                b_spider = models.Spider.objects.filter(target_domain=domain)
                if not b_spider:
                    m_spider = models.Spider(target_domain=domain)
                    args['spider_flag'] = True
                    if 'spider_thread' in params.keys():
                        m_spider.spider_thread = params['spider_thread']
                        args['spider_thread'] = int(params['spider_thread'])
                        # spider_thread_num = params['spider_thread']
                        # new_spider(target, spider_thread_num)
                    m_spider.save()
                    args['target_url'] = target
                    args['spider_id'] = m_spider.id
                    m_single_task.spider_id = m_spider.id
                else:
                    args['spider_flag'] = False

            if 'exploit_flag' in params.keys():
                b_exploit = models.ExploitAttack.objects.filter(target_domain=domain)
                if not b_exploit:
                    args['exploit_flag'] = True
                    m_exploit_attack = models.ExploitAttack(target_domain=target)
                    m_exploit_attack.save()
                    args['exploit_url'] = '/'.join(target.split('/')[:3])
                    args['exploit_id'] = m_exploit_attack.id
                    # new_exploit_attack(target)
                    m_single_task.exploit_id = m_exploit_attack.id
                else:
                    args['exploit_flag'] = False

            m_single_task.save()
            args['task_id'] = m_single_task.id
            # json_args = json.dumps(dict(params))
            json_args = json.dumps(args)
            json_args = json_args.replace('"', "'")
            work = 'python ' + CORE_PATH + os.sep + 'worker.py ' + json_args
            p = subprocess.Popen(work)
            print 'open success:', p
            # print params
            return HttpResponse("任务开启成功")
        except Exception as e:
            print e
            return HttpResponse("任务开启失败")


def new_batch_web_task(request):
    return render(request, 'task/new_batch_task.html')


def task_list(request):
    return render(request, 'task/task_list.html')


def show_task(request):
    return render(request, 'task/show_task.html')


def new_single_web_task(request):
    if not request.user.is_authenticated():
        return HttpResponse("<div style='text-align:center;margin-top:20%'><h3>请登录</h3><br><br><a href='/user/login/'>点击跳转到登陆页面</a>")
    if request.method == 'GET':
        return render(request, 'task/new_single_task.html')
    if request.method == 'POST':
        params = request.POST
        try:
            if 'target' not in params:
                return HttpResponse("目标错误")
            args = {}
            target = params['target']
            target = get_root_url(target)
            args['target'] = target
            domain = get_domain(target)
            first_domain = get_first_domain(domain)
            ipaddrs = []
            try:
                ipaddrs = get_ip(domain)
            except Exception as e:
                print e
            ips = models.DomainIP.objects.filter(domain=domain).values('ip')
            for ip in ips:
                if ip['ip'] not in ipaddrs:
                    m_domainip = models.DomainIP(first_domain=first_domain, domain=domain, ip=ip)
                    m_domainip.save()

            m_web_single_task = models.WebSingleTask(target_url=target)
            m_web_single_task.save()

            # 判断数据库是否已经有该域名的指纹识别了，如果有，则不在进行识别，防止多个用户对同一个目标进行多次测试。
            #finger
            b_finger = models.Finger.objects.filter(target_domain=domain)
            if b_finger:
                args['finger_flag'] = False
            else:
                args['finger_flag'] = True
                m_finger = models.Finger(target_domain=domain, target_url=target)
                m_finger.save()
                args['finger_id'] = m_finger.id
                args['finger_target_url'] = target
                m_web_single_task.finger_id = m_finger.id

            #exploit
            # 判断数据库是否已经有该域名的web攻击测试了，如果有，则不在进行测试
            b_exploit = models.WebExploit.objects.filter(target_domain=domain)
            if b_exploit:
                args['exploit_flag'] = False
            else:
                args['exploit_flag'] = True
                m_exploit_attack = models.WebExploit(target_url=target, target_domain=domain)
                m_exploit_attack.save()
                args['exploit_url'] = target
                args['exploit_id'] = m_exploit_attack.id
                # new_exploit_attack(target)
                m_web_single_task.exploit_id = m_exploit_attack.id

            m_web_single_task.save()
            args['task_id'] = m_web_single_task.id
            args['model'] = 1
            json_args = json.dumps(args)
            json_args = json_args.replace('"', "'")
            # work = 'python ' + CORE_PATH + os.sep + 'worker.py ' + json_args
            work = 'python ' + CORE_PATH + os.sep + 'core.py ' + json_args
            p = subprocess.Popen(work)
            print 'open success:', p
            # print params
            return HttpResponse("任务开启成功")
        except Exception as e:
            print e
            return HttpResponse("任务开启失败")


"""
r_ result
b_ boolean
m_ my
"""


def web_task_info(request, id):
    # print id
    args = {}
    task = models.WebSingleTask.objects.filter(id=id)
    target_url = task[0].target_url
    status = task[0].status
    update_date = task[0].update_date
    args['id'] = id
    args['target_url'] = target_url
    args['status'] = status
    args['update_date'] = update_date

    finger_id = task[0].finger_id
    exploit_id = task[0].exploit_id

    if finger_id is 0:
        args['b_finger'] = False
    else:
        args['b_finger'] = True
        finger_args = {}
        finger_obj = models.Finger.objects.get(id=finger_id)
        finger_domain = finger_obj.target_domain
        finger_args['domain'] = finger_domain
        finger_status = finger_obj.status
        finger_args['status'] = finger_status
        if finger_status == 2:
            apptypes = models.AppType.objects.filter(domain=finger_domain)
            app_list = []
            for apptype in apptypes:
                app = {}
                app['name'] = apptype.name
                app['cata'] = apptype.cata
                app['implies'] = apptype.implies
                app_list.append(app)
            finger_args['app_num'] = len(apptypes)
            finger_args['app_list'] = app_list
        else:
            finger_count = finger_obj.finger_count
            finger_current = finger_obj.current_index
            finger_rate = finger_current * 100 / finger_count
            finger_args['rate'] = finger_rate
        args['r_finger'] = finger_args
    if exploit_id is 0:
        args['b_exploit'] = False
    else:
        args['b_exploit'] = True
        exp_args = {}
        exp_obj = models.WebExploit.objects.get(id=exploit_id)
        target_url = exp_obj.target_url
        target_domain = exp_obj.target_domain
        status = exp_obj.status
        exp_args['status'] = status
        if status == 2:
            exp_result_objs = models.WebExploitResult.objects.filter(domain=target_domain)
            exp_results = []
            for exp_result_obj in exp_result_objs:
                result = {}
                result['type'] = exp_result_obj.exp_type
                result['name'] = exp_result_obj.exp_name
                exp_results.append(result)
            exp_args['result'] = exp_results
            exp_args['result_num'] = len(exp_result_objs)
        args['r_exploit'] = exp_args
    return render(request, 'task/task_info.html', {"info": args})


def finger(request):
    return render(request, 'scan/finger.html', {"test": "test"})
    # return HttpResponse("finger")


def port_scan(request):
    return render(request, 'scan/port_scan.html')
    # return HttpResponse("port")


def exploit_attack(request):
    return render(request, 'scan/exploit_attack.html')
    # return HttpResponse("poc")


def spider(request):
    return render(request, 'scan/spider.html')
    # return HttpResponse("spider")


def domain_brute(request):
    return render(request, 'scan/domain_brute.html')


def fuzz(request):
    return HttpResponse("fuzz")


# http://v3.bootcss.com/examples/theme/#
# http://v3.bootcss.com/components/
# http://www.bootcss.com/
# http://v3.bootcss.com/examples/dashboard/


def view_web_task_list(request):

    tasklist = []
    single_task = WebSingleTask.objects.all()
    for task in single_task:
        a_task = {}
        a_task['id'] = task.id
        a_task['target_url'] = task.target_url
        a_task['status'] = task.status
        a_task['update_date'] = task.update_date
        a_task['type'] = 0      # 0表示单个，1表示批量

        tasklist.append(a_task)
    return render(request, 'task/view_web_task.html', {'tasks': tasklist})


def new_single_sys_task(request):
    return HttpResponse("新建系统测试任务")


def new_batch_sys_task(request):
    return HttpResponse("新建批量系统测试任务")


def view_sys_task_list(request):
    return HttpResponse("系统任务列表")


def port_scan(request):
    return HttpResponse("端口扫描")


def web_spider(request):
    return HttpResponse("网页爬虫")


def domain_brute(request):
    return HttpResponse("域名爆破")


def view_single_task(request):
    tasklist = []
    single_task = SingleTask.objects.all()
    for task in single_task:
        a_task = {}
        a_task['id'] = task.id
        a_task['target_url'] = task.target_url
        a_task['status'] = task.task_status
        a_task['update_date'] = task.update_date
        a_task['type'] = 0      # 0 表示单个，1表示批量
        tasklist.append(a_task)
    return render(request, 'task/view_single_task.html', {'tasks': tasklist})


def view_batch_task(request):
    return render(request, 'task/view_batch_task.html')