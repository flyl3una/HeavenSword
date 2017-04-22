# coding=utf-8
import json
import md5
import os
import random
import socket
import string
import subprocess

import time

import datetime

import cStringIO
from PIL import Image, ImageDraw, ImageFont
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.core.files import File
from django.core.mail import send_mail
from django.db.models import FileField
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

from HeavenSword.settings import DEFAULT_FROM_EMAIL, EMAIL_HOST_USER, TOOLS_PATH, STATIC_PATH, UPLOAD_PATH
from tools.Spider import Tree
from tools.config import FINGER_PATH
from tools.function import get_ip, get_domain, get_first_domain, get_root_url, get_father_domain
from web import models
from web.dir.EmailToken import EmailToken
from web.models import WebSingleTask, PortScan, DomainBrute, Spider, UserTaskId, UserPower, UserSetting, Finger, \
    UploadPoc
from web.msetting import DOMAIN, PORT_MODEL, PORT_THREAD, DOMAIN_MODEL, DOMAIN_THREAD, SPIDER_THREAD


def auth(request):
    if request.user.is_authenticated():
        return True
    else:
        return False


def index(request):
    if not auth(request):
        return HttpResponseRedirect('/user/login/')
    username = ''
    apptags = models.AppTag.objects.all()
    if not apptags:
        json_file_path = os.path.join(FINGER_PATH, 'apps.json')
        # 获取指纹json字典
        fp = file(json_file_path)
        tags = json.load(fp, encoding='utf-8')
        fp.close()
        app_count = len(tags[u'apps'])
        cata_count = len(tags[u'categories'])
        if app_count == 0 or cata_count == 0:
            print '没有指纹识别配置文件'
            return HttpResponse("服务器配置文件缺失，请联系管理员")
        for key, value in tags[u'apps'].items():
            catas = value[u'cats']
            cats = []
            [cats.append(tags[u'categories'][str(i)]) for i in catas]
            cats_str = '|'.join(cats)
            tag = models.AppTag(name=key, cata=cats_str)
            tag.save()

    if request.method == 'GET':
        if request.user.is_authenticated():
            username = request.COOKIES.get("username")
        return render(request, 'index.html', {'username': username})
    if request.method == 'POST':
        url = request.POST.get('target')
        # print url
        return new_single_web_task(request)
        # return render(request, 'index.html', {'username': username})


def captcha(request):
    '''Captcha'''
    image = Image.new('RGB', (100, 40), color=(random.randint(32, 127), random.randint(32, 127), random.randint(32, 127)))  # model, size, background color
    font_file = os.path.join(STATIC_PATH, 'fonts', 'monaco.ttf')   # choose a font file
    font = ImageFont.truetype(font_file, 30)    # the font object
    draw = ImageDraw.Draw(image)
    rand_str = ''.join(random.sample(string.letters + string.digits, random.randint(4, 5)))    # The random string
    # print rand_str
    draw.text((7, 0), rand_str, fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), font=font)  # position, content, color, font
    # 干扰线
    for i in range(8):
        draw.line([random.randint(0, 120), random.randint(0, 40), random.randint(0, 120), random.randint(0, 40)], fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), width=1)
    # g.setColor(new Color(r.nextInt(256), r.nextInt(256), r.nextInt(256)));
    # // 画线
    # g.drawLine(r.nextInt(120), r.nextInt(30), r.nextInt(120), r.nextInt(30));
    del draw
    request.session['captcha'] = rand_str.lower()   # store the content in Django's session store
    buf = cStringIO.StringIO()  # a memory buffer used to store the generated image
    image.save(buf, 'jpeg')
    return HttpResponse(buf.getvalue(), 'image/jpeg') # return the image data stream as image/jpeg format, browser will treat it as an image


def user_login(request):
    # if request.user.is_authenticated():
    #     return HttpResponseRedirect('/')

    if request.method == 'GET':
        return render(request, 'user/login1.html')
    if request.method == 'POST':
        # username = request.POST.get('username')
        captcha_code = request.POST.get('captcha_code')
        if captcha_code.lower() != request.session.get('captcha'):
            error = "验证码不正确，请重新输入。"
            return HttpResponse('<script>parent.login_result_error("'+error+'");</script>')
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = User.objects.get(email=email).get_username()
        user = authenticate(username=username, password=password)
        # print email, password
        if user:
            if user.is_active:
                logout(request)
                login(request, user)

                # response = HttpResponseRedirect('/')
                response = HttpResponse('<script>parent.login_result_success();</script>')
                response.set_cookie('username', username, max_age=None)
                # return redirect(reverse('views.index'), args=[])
                return response
            else:
                error = "账号未激活，请到邮箱激活账户。"
                return HttpResponse('<script>parent.login_result_error("' + error + '");</script>')
        else:
            print "Invalid login details: {0}, {1}".format(email, password)
            error = '密码错误'
            return HttpResponse('<script>parent.login_result_error("' + error + '");</script>')


def user_logout(request):
    auth(request)
    logout(request)
    # return render(request, '/')
    return HttpResponseRedirect('/')


def user_register(request):
    if request.method == 'GET':
        return render(request, 'user/register.html')
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
            if len(password) <= 8:
                return HttpResponse("<script>parent.register_error3();</script>")
        user = User(username=username, email=email)
        user.set_password(password)
        user.is_active = False

        token_confirm = EmailToken('xqlpniip)kgj&dod5e=k95!q6su!m$tsy__&li3-vx)tflp#yr')
        token = token_confirm.generate_validate_token(email)
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
        email = token_confirm.confirm_validate_token(token)
    except:
        user = User.objects.get(email=email)
        user.delete()
        return HttpResponse("连接已超时，请重新注册。")
    try:
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()
        user_power = UserPower(user)
        user_setting = UserSetting(user)
        user_power.save()
        user_setting.save()
        return HttpResponse("账号激活成功。<br><a href='/user/login/'>点击跳转到登陆页面</a>")
    except:
        return HttpResponse("该邮箱没有被注册。")


def user_find_pwd(request):
    if request.method == 'GET':
        return render(request, 'user/find_pwd.html')
    elif request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            info = '更改密码邮件已发送，请登录邮箱按邮件操作。'

            username = user.username
            token_confirm = EmailToken('xqlpniip)kgj&dod5e=k95!q6su!m$tsy__&li3-vx)tflp#yr')
            token = token_confirm.generate_validate_token(email)
            # active_key = base64.encodestring(username)
            # send email to the register email
            message = "\n".join([
                u'{0},欢迎使用倚天剑'.format(username),
                u'请访问该链接，重新修改密码:',
                '/'.join([DOMAIN, 'user/reset_pwd', token])
            ])
            from_email = EMAIL_HOST_USER
            send_mail(u'注册用户验证信息', message, from_email, [email])
            user.save()

        except Exception as e:
            print e
            info = '该邮箱地址没被注册过，请重新输入。'
        return HttpResponse("<script>parent.find_pwd_info('"+info+"')</script>")


def user_reset_pwd_post(request):
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1 and password1 != '' and password1 == password2:
            try:
                user = User.objects.get(email=email)
                user.set_password(password1)
                user.save()
                return HttpResponse("<script>parent.reset_success()</script>")
            except Exception as e:
                print e
                return HttpResponse("该邮箱不存在")
        else:
            info = '两次密码不相同，请重新输入。'
            return HttpResponse("<script>parent.reset_fails_info('" + info + "')</script>")


def user_reset_pwd(request, token):
    if request.method == 'GET':
        token_confirm = EmailToken('xqlpniip)kgj&dod5e=k95!q6su!m$tsy__&li3-vx)tflp#yr')
        email = token_confirm.confirm_validate_token(token)
        try:
            user = User.objects.get(email=email)
            return render(request, 'user/user_reset_pwd.html', {"user": user})
        except Exception as e:
            print e
            return HttpResponse("该邮箱不存在")


def user_info(request):
    if not auth(request):
        return HttpResponseRedirect('/user/login/')
    if request.method == 'GET':
        user = request.user
        tags = models.AppTag.objects.all()
        return render(request, 'user/user_info.html', {"user": user, "tags": tags})
    elif request.method == 'POST':
        params = request.POST
        pwd = params['password']
        pwd1 = params['password1']
        pwd2 = params['password2']
        if pwd1 and pwd1 != '' and pwd1 != pwd2:
            error = '两次密码不相同，请重新输入。'
            return HttpResponse("<script>parent.show_change_pwd_error('"+error+"')</script>")
        user = request.user
        username = user.username
        user1 = authenticate(username=username, password=pwd)
        if user1:
            user.set_password(pwd1)
            user.save()
            logout(request)
            return HttpResponse("<script>parent.change_pwd_success()</script>")


def upload_poc(request):
    if not auth(request):
        return HttpResponseRedirect('/user/login/')
    if request.method == 'GET':
        return HttpResponse("页面错误")
    elif request.method == 'POST':
        params = request.POST
        pocname = params['pocname']
        apptag = params['apptag']
        try:
            tag = models.AppTag.objects.get(id=int(apptag))

            pocdesc = params['pocdesc']
            # poc_file = params['poc_file']
            file_obj = request.FILES.get("poc_file")
            if not file_obj:
                return HttpResponse('<script>parent.window.alert_info("请选择文件");</script>')
            filename = file_obj.name
            # 文件扩展名
            ext = os.path.splitext(filename)[1]
            if ext != '.py':
                return HttpResponse('<script>parent.window.alert_info("文件名错误");</script>')
            # file = models.UploadPoc(user=request.user, app_tag=tag, poc_name=pocname, poc_desc=pocdesc, poc_file=file_obj)

            # 定义文件名，年月日时分秒随机数
            fn = time.strftime("%Y%m%d%H%M%S")
            fn = fn + "_%d" % random.randint(0, 100)
            # 重写合成文件名
            name = os.path.join(fn + ext)
            file_full_path = os.path.join(UPLOAD_PATH, name)
            dest = open(file_full_path, 'wb+')
            file_content = file_obj.read()
            dest.write(file_content)
            dest.close()
            file = models.UploadPoc(user=request.user, app_tag=tag, poc_name=pocname, poc_desc=pocdesc, poc_path=name, file_content=file_content)
            file.save()
            return HttpResponse('<script>parent.window.alert_info("上传成功");</script>')
            # return HttpResponseRedirect("/user/info/")
        except Exception as e:
            return HttpResponse('<script>parent.window.alert_info("错误");</script>')


def identify_poc(request):
    return render_to_response(
        "admin/identify_poc.html",
        {'poc_list': UploadPoc.objects.all()},
        RequestContext(request, {}),
    )
    report = staff_member_required(report)


#先修改上传文件后返回poc_name，然后在更改返回值字段。
def show_poc(request, id):
    if not auth(request):
        return HttpResponseRedirect('/user/login/')
    if request.method == 'GET':
        args = {}
        try:
            poc_obj = models.UploadPoc.objects.get(id=int(id))
            content = poc_obj.file_content
            status = 1
        except Exception as e:
            print e
            content = ''
            status = 0
        args['status'] = status
        args['content'] = content
        return JsonResponse(json.dumps(args), safe=False)


def help(request):
    return render(request, 'help.html')


# def batch(request):
#     return render(request, 'batch.html')


def operation(request):
    if not auth(request):
        return HttpResponseRedirect('/user/login/')
    if request.method == 'GET':
        if request.user.is_authenticated():
            username = request.COOKIES.get("username")
            params = {}
            params['username'] = username
            if request.user.is_superuser:
                admin = True
                params['admin'] = admin
            b_power = UserPower.objects.filter(user=request.user)
            if b_power:
                # params['b_power'] = True
                params['r_power'] = b_power[0]
            else:
                r_power = UserPower(user=request.user)
                r_power.save()
                params['r_power'] = r_power
            b_setting = UserSetting.objects.filter(user=request.user)
            if not b_setting:
                user_setting = UserSetting(user=request.user)
                user_setting.save()
            return render(request, 'operation.html', {'params': params})
    return HttpResponse("<div style='text-align:center;margin-top:20%'><h3>请登录</h3><br><br><a href='/user/login/'>点击跳转到登陆页面</a>")


def auth_power(user, field):
    flag = False
    try:
        user_power = UserPower.objects.get(user=user)
        flag = user_power.__getattribute__(field)
    except Exception as e:
        print e
        flag = False
    return flag


def new_batch_web_task(request):
    if not auth(request):
        return HttpResponseRedirect('/user/login/')
    flag = auth_power(request.user, 'batch_web_task')
    if not flag:
        return HttpResponse('<script>alert("你没有该操作的权限")</script>')
    if request.method == 'GET':
        return render(request, 'task/new_batch_web_task.html')
    elif request.method == 'POST':
        # try:
        params = request.POST
        # print params['urls']
        targets = params['urls'].split(',')
        # except:
        #     return HttpResponse('<script>parent.new_web_batch_form_result("任务开启失败")<script>')
        str = ''
        for target in targets:
            flag1 = new_web_task(target, request.user)
            if flag1:
                str += target + '开启成功<br>'
            else:
                str += target + '开始失败<br>'
        return HttpResponse('<script>parent.new_web_batch_form_result("' + str + '")</script>')


# def task_list(request):
#     return render(request, 'task/task_list.html')


# def show_task(request):
#     return render(request, 'task/show_task.html')


def new_web_task(target, user):
    try:
        args = {}
        target = get_root_url(target)
        args['target'] = target
        domain = get_domain(target)
        first_domain = get_first_domain(domain)
        b_web_single_task = WebSingleTask.objects.filter(domain=domain)
        if b_web_single_task:
            # task_id = b_web_single_task[0].id
            # user_id = user.id
            task_obj = WebSingleTask.objects.get(domain=domain)
            b_user_task_id = UserTaskId.objects.filter(user=user, task=task_obj)
            if b_user_task_id:
                return True
            user_task_id = UserTaskId(task=task_obj, user=user)
            user_task_id.save()
            return True
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

        m_web_single_task = models.WebSingleTask(target_url=target, domain=domain)
        m_web_single_task.save()

        # 判断数据库是否已经有该域名的指纹识别了，如果有，则不在进行识别，防止多个用户对同一个目标进行多次测试。
        # finger
        b_finger = models.Finger.objects.filter(target_domain=domain)
        if b_finger:
            args['finger_flag'] = False
            m_web_single_task.finger_id = b_finger[0].id
        else:
            args['finger_flag'] = True
            m_finger = models.Finger(target_domain=domain, target_url=target)
            m_finger.save()
            args['finger_id'] = m_finger.id
            args['finger_target_url'] = target
            m_web_single_task.finger_id = m_finger.id

        # exploit
        # 判断数据库是否已经有该域名的web攻击测试了，如果有，则不在进行测试
        b_proof = models.WebProof.objects.filter(target_domain=domain)
        if b_proof:
            args['proof_flag'] = False
            m_web_single_task.proof_id = b_proof[0].id
        else:
            args['proof_flag'] = True
            m_proof_attack = models.WebProof(target_url=target, target_domain=domain)
            m_proof_attack.save()
            args['proof_url'] = target
            args['proof_id'] = m_proof_attack.id
            # new_exploit_attack(target)
            m_web_single_task.proof_id = m_proof_attack.id

        m_web_single_task.save()
        m_user_task_id = UserTaskId(user=user, task=m_web_single_task)
        m_user_task_id.save()
        args['task_id'] = m_web_single_task.id
        args['model'] = 1
        json_args = json.dumps(args)
        json_args = json_args.replace('"', "'")
        work = 'python ' + TOOLS_PATH + os.sep + 'core.py ' + json_args
        p = subprocess.Popen(work)
        print 'open success:', p
        # print params
        return True
        # return HttpResponseRedirect(view_web_task_list(request))
    except Exception as e:
        print e
        return False


def new_single_web_task(request):
    if not auth(request):
        return HttpResponseRedirect('/user/login/')
    flag = auth_power(request.user, 'single_web_task')
    if not flag:
        return HttpResponse('<script>alert("你没有该操作的权限")</script>')
    if request.method == 'GET':
        return render(request, 'task/new_single_web_task.html')
    if request.method == 'POST':
        params = request.POST
        if 'target' not in params:
            # '<script>parent.new_web_single_form_result("目标错误")</script>'
            return HttpResponse('<script>parent.new_web_single_form_result("目标错误")</script>')
        target = params['target']
        flag = new_web_task(target, request.user)
        if flag:
            return HttpResponse('<script>parent.new_web_single_form_result("任务开启成功")</script>')
        else:
            return HttpResponse('<script>parent.new_web_single_form_result("任务开启失败")</script>')


def view_web_task_list(request):
    if not auth(request):
        return HttpResponseRedirect('/user/login/')
    tasklist = []
    # single_task = WebSingleTask.objects.all()
    user_task = UserTaskId.objects.filter(user=request.user)

    for single_task in user_task:
        task = WebSingleTask.objects.get(id=single_task.task_id)
        a_task = {}
        a_task['id'] = task.id
        a_task['target_url'] = task.target_url
        a_task['status'] = task.status
        a_task['update_date'] = task.update_date
        a_task['type'] = 0      # 0表示单个，1表示批量

        tasklist.append(a_task)
    return render(request, 'task/view_web_task.html', {'tasks': tasklist})


"""
r_ result
b_ boolean
m_ my
"""


def web_task_info(request, id):
    if not auth(request):
        return HttpResponseRedirect('/user/login/')
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
    proof_id = task[0].proof_id

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
    if proof_id is 0:
        args['b_proof'] = False
    else:
        args['b_proof'] = True
        poc_args = {}
        poc_obj = models.WebProof.objects.get(id=proof_id)
        target_url = poc_obj.target_url
        target_domain = poc_obj.target_domain
        status = poc_obj.status
        poc_args['status'] = status
        if status == 2:
            poc_result_objs = models.WebProofResult.objects.filter(domain=target_domain)
            poc_results = []
            for poc_result_obj in poc_result_objs:
                result = {}
                result['type'] = poc_result_obj.poc_type
                name = poc_result_obj.poc_name
                try:
                    poc = models.UploadPoc.objects.get(poc_path=name)
                    result['name'] = poc.poc_name
                    result['id'] = poc.id
                except Exception as e:
                    print e
                    result['name'] = name
                    result['id'] = 0
                poc_results.append(result)
            poc_args['result'] = poc_results
            poc_args['result_num'] = len(poc_result_objs)
        args['r_proof'] = poc_args
    return render(request, 'task/task_info.html', {"info": args})


# def finger(request):
#     return render(request, 'tools/finger.html', {"test": "test"})
    # return HttpResponse("finger")


# def get_port_result(request, ip):
#     return render(request, 'tools/port_scan.html')


#查看端口扫描结果
def view_finger(request, id):
    if not auth(request):
        return HttpResponseRedirect('/user/login/')
    args = {}
    try:
        finger = models.Finger.objects.get(id=id)
    except Exception as e:
        print e
        args['flag'] = 0
        args['info'] = "没有找到该任务"
    else:
        if finger.status != 2:
            args['flag'] = 1
            args['info'] = "扫描未完成，请耐心等待"
            args['rate'] = finger.current_index * 100 / finger.finger_count
        else:
            result_list = []
            apptypes = models.AppType.objects.filter(domain=finger.target_domain)
            for apptype in apptypes:
                dic = {}
                dic['cata'] = apptype.cata
                dic['name'] = apptype.name
                result_list.append(dic)
            args['flag'] = 2
            args['result_list'] = result_list
    return JsonResponse(json.dumps(args), safe=False)


def finger(request):
    if not auth(request):
        return HttpResponseRedirect('/user/login/')
    flag = auth_power(request.user, 'port_scan')
    if not flag:
        return HttpResponse('<script>alert("你没有该操作的权限")</script>')
    if request.method == 'GET':
        return render(request, 'tools/finger.html')
    elif request.method == 'POST':
        params = request.POST
        json_dic = {}
        try:
            if 'id' in params and int(params['id']) != 0:
                id = int(params['id'])
                finger_obj = models.Finger.objects.get(id=id)
                if finger.status != 2:
                    json_dic['flag'] = 0
                    json_dic['info'] = "请等待目前任务执行完成"
                    return HttpResponse("<script>parent.finger_form_result('" + json.dumps(json_dic) + "');</script>")
            if 'url' not in params:
                return HttpResponse("<script>parent.show_error('请输入目标url');</script>")

            # 开启指纹识别任务
            url = params['url']
            domain = get_domain(url)
            target_url = get_root_url(url)
            finger_objs = models.Finger.objects.filter(target_domain=domain)
            if not finger_objs:
                args = {}
                finger_obj = Finger(target_domain=domain, target_url=url)
                finger_obj.save()
                finger_id = finger_obj.id

                args['finger_id'] = finger_id
                args['domain'] = domain
                args['target_url'] = url
                args['model'] = 10
                json_args = json.dumps(args)
                json_args = json_args.replace('"', "'")
                work = 'python ' + TOOLS_PATH + os.sep + 'core.py ' + json_args
                p = subprocess.Popen(work)
                print 'open success:', p
            else:
                #已有该记录
                if finger_objs[0].status == 2:
                    result_list = []
                    apptypes = models.AppType.objects.filter(domain=domain)
                    for app in apptypes:
                        dic = {}
                        dic['name'] = app.name
                        dic['cata'] = app.cata
                        dic['implies'] = app.implies
                        result_list.append(dic)
                    json_dic['id'] = 0
                    json_dic['flag'] = 2
                    json_dic['info'] = '指纹识别完成'
                    json_dic['result_list'] = result_list
                    return HttpResponse(
                        "<script>parent.finger_form_result('" + json.dumps(json_dic) + "');</script>")
                else:
                    finger_id = finger_objs[0].id
            json_dic['id'] = finger_id
            json_dic['info'] = "指纹识别开启成功"
            json_dic['flag'] = 1
            return HttpResponse(
                "<script>parent.finger_form_result('" + json.dumps(json_dic) + "');</script>")
        except Exception as e:
            print e
            json_dic['info'] = "指纹识别开启失败"
            json_dic['flag'] = 0
            return HttpResponse("<script>parent.finger_form_result('" + json.dumps(json_dic) + "');</script>")


#查看端口扫描结果
def view_port_scan(request, id):
    if not auth(request):
        return HttpResponseRedirect('/user/login/')
    args = {}
    try:
        portscan = models.PortScan.objects.get(id=id)
    except Exception as e:
        print e
        args['flag'] = 0
        args['info'] = "没有找到该任务"
        # HttpResponse('<script>form_result("请等待目前任务执行完成");</script>')
    else:
        openports = models.OpenPort.objects.filter(ip_addr=portscan.target_ip)
        if not openports:
            args['flag'] = 1
            args['info'] = "扫描未完成，请耐心等待"
            args['rate'] = portscan.current_index * 100 / portscan.port_count
        else:
            result_list = []
            for openport in openports:
                dic = {}
                dic['port'] = openport.port_num
                dic['info'] = openport.port_info
                result_list.append(dic)
            args['flag'] = 2
            args['result_list'] = result_list
    return JsonResponse(json.dumps(args), safe=False)


def port_scan(request):
    if not auth(request):
        return HttpResponseRedirect('/user/login/')
    flag = auth_power(request.user, 'port_scan')
    if not flag:
        return HttpResponse('<script>alert("你没有该操作的权限")</script>')
    if request.method == 'GET':
        return render(request, 'tools/port_scan.html')
    elif request.method == 'POST':
        params = request.POST
        # 开启新端口扫描任务
        json_dic = {}
        try:
            if 'id' in params and int(params['id']) != 0:
                id = int(params['id'])
                port_scan_obj = models.PortScan.objects.get(id=id)
                if port_scan_obj.status != 2:
                    json_dic['flag'] = 0
                    json_dic['info'] = "请等待目前任务执行完成"
                    return HttpResponse("<script>parent.port_scan_form_result('" + json.dumps(json_dic) + "');</script>")
            if 'ip' not in params:
                # return render(request, 'tools/port_scan.html', {"error": "请输入ip地址"})
                return HttpResponse("<script>parent.show_error('请输入ip地址');</script>")

            # 开启新端口扫描任务
            #判断ip格式
            ip_addr = params['ip']
            flag = False
            try:
                ips = ip_addr.split('.')
                if len(ips) != 4:
                    flag = True
                int_ips = []
                for ip in ips:
                    int_ip = int(ip)
                    if int_ip > 255 or int_ip < 0:
                        flag = True
                    int_ips.append(int_ip)
            except:
                flag = True
            if flag:
                # return render(request, 'tools/port_scan.html', {"error": "ip地址格式不正确"})
                return HttpResponse("<script>parent.show_error('ip地址格式不正确');</script>")
            else:
                port_scan_objs = models.PortScan.objects.filter(target_ip=ip_addr)
                if not port_scan_objs:
                    args = {}
                    user_setting = UserSetting.objects.get(user=request.user)
                    args['port_scan_model'] = user_setting.port_scan_model # PORT_MODEL #all usually
                    args['port_scan_thread'] = user_setting.port_scan_thread #PORT_THREAD
                    port_scan_obj = PortScan(target_ip=ip_addr, thread=args['port_scan_thread'], model=args['port_scan_model'])
                    port_scan_obj.save()
                    port_scan_id = port_scan_obj.id
                    args['port_scan_id'] = port_scan_obj.id
                    args['ip'] = ip_addr
                    args['model'] = 11
                    json_args = json.dumps(args)
                    json_args = json_args.replace('"', "'")
                    work = 'python ' + TOOLS_PATH + os.sep + 'core.py ' + json_args
                    p = subprocess.Popen(work)
                    print 'open success:', p
                else:
                    # 已有该ip记录
                    if port_scan_objs[0].status == 2:
                        # id = port_scan_objs[0].id
                        # return view_port_scan(request, id)
                        # json_dic['info'] = "任务执行完成"
                        # json_dic['id'] = id
                        # id = port_scan_obj.id
                        openports = models.OpenPort.objects.filter(ip_addr=ip_addr)
                        result_list = []
                        for openport in openports:
                            dic = {}
                            dic['port'] = openport.port_num
                            dic['info'] = openport.port_info
                            result_list.append(dic)
                        json_dic['id'] = 0
                        json_dic['flag'] = 2
                        json_dic['info'] = "端口扫描完成"
                        json_dic['result_list'] = result_list
                        return HttpResponse("<script>parent.port_scan_form_result('" + json.dumps(json_dic) + "');</script>")
                    else:
                        port_scan_id = port_scan_objs[0].id
                json_dic['id'] = port_scan_id
                json_dic['info'] = "端口扫描开启成功"
                json_dic['flag'] = 1
                return HttpResponse("<script>parent.port_scan_form_result('" + json.dumps(json_dic) + "');</script>")
        except Exception as e:
            print e
            json_dic['info'] = "端口扫描开启失败"
            json_dic['flag'] = 0
            return HttpResponse("<script>parent.port_scan_form_result('" + json.dumps(json_dic) + "');</script>")


#查看端口扫描结果
def view_domain_brute(request, id):
    if not auth(request):
        return HttpResponseRedirect('/user/login/')
    args = {}
    try:
        domainbrute = models.DomainBrute.objects.get(id=id)
    except Exception as e:
        print e
        args['flag'] = 0
        args['info'] = "没有找到该任务"
        # HttpResponse('<script>form_result("请等待目前任务执行完成");</script>')
    else:
        domainips = models.DomainIP.objects.filter(first_domain=domainbrute.target_first_domain)
        if domainbrute.status != 2:
            args['flag'] = 1
            args['info'] = "扫描未完成，请耐心等待"
            args['rate'] = domainbrute.current_index * 100 / domainbrute.domain_count
        else:
            args['flag'] = 2
            args['rate'] = 100
        result_dic = {}
        for domainip in domainips:
            dic = {}
            domain = domainip.domain
            ip = domainip.ip
            dic['domain'] = domainip.domain
            if domain in result_dic.keys():
                if ip not in result_dic[domain]:
                    result_dic[domain].append(ip)
            else:
                result_dic[domain] = [ip]
        args['result_dic'] = result_dic
    return JsonResponse(json.dumps(args), safe=False)


def domain_brute(request):
    if not auth(request):
        return HttpResponseRedirect('/user/login/')
    flag = auth_power(request.user, 'domain_brute')
    if not flag:
        return HttpResponse('<script>alert("你没有该操作的权限")</script>')
    if request.method == 'GET':
        return render(request, 'tools/domain_brute.html')
    elif request.method == 'POST':
        params = request.POST
        # 开启新域名爆破任务
        json_dic = {}
        try:
            if 'id' in params and int(params['id']) != 0:
                id = int(params['id'])
                domain_brute_obj = models.DomainBrute.objects.get(id=id)
                if domain_brute_obj.status != 2:
                    json_dic['flag'] = 0
                    json_dic['info'] = "请等待目前任务执行完成"
                    HttpResponse("<script>parent.domain_brute_form_result('" + json.dumps(json_dic) + "');</script>")
                # elif domain_brute_obj.status == 2:
                #     return render(request, "tools/domain_brute.html")
                # return HttpResponse("<script>parent.form_result('" + json.dumps(json_dic) + "');</script>")
            if 'domain' not in params:
                return HttpResponse("<script>parent.show_error('请输入域名');</script>")
            # 开启新端口扫描任务
            domain = params['domain']
            domain = get_domain(domain)
            first_domain = get_father_domain(domain)
            domain_brute_objs = models.DomainBrute.objects.filter(target_first_domain=first_domain)
            if not domain_brute_objs:
                args = {}
                user_setting = UserSetting.objects.get(user=request.user)
                args['domain_brute_model'] = user_setting.domain_brute_model # DOMAIN_MODEL  # all usually
                args['domain_brute_thread'] = user_setting.domain_brute_thread # DOMAIN_THREAD
                domain_brute_obj = DomainBrute(target_first_domain=first_domain, target_domain=domain, model=args['domain_brute_model'], thread=args['domain_brute_thread'])
                domain_brute_obj.save()
                domain_brute_obj_id = domain_brute_obj.id
                args['domain_brute_id'] = domain_brute_obj.id
                args['first_domain'] = first_domain
                args['model'] = 12
                json_args = json.dumps(args)
                json_args = json_args.replace('"', "'")
                work = 'python ' + TOOLS_PATH + os.sep + 'core.py ' + json_args
                p = subprocess.Popen(work)
                print 'open success:', p
            else:
                if domain_brute_objs[0].status == 2:
                    first_domain = domain_brute_objs[0].target_first_domain
                    domain_ip_objs = models.DomainIP.objects.filter(first_domain=first_domain)
                    results = {}
                    for domain_ip_obj in domain_ip_objs:
                        domain = domain_ip_obj.domain
                        ip = domain_ip_obj.ip
                        if domain in results.keys():
                            if ip not in results[domain]:
                                results[domain].append(ip)
                        else:
                            results[domain] = [ip]
                    json_dic['flag'] = 2
                    json_dic['id'] = 0
                    json_dic['info'] = '端口扫描完成'
                    json_dic['result_dic'] = results
                    return HttpResponse("<script>parent.domain_brute_form_result('" + json.dumps(json_dic) + "');</script>")
                else:
                    domain_brute_obj_id = domain_brute_objs[0].id
            json_dic['id'] = domain_brute_obj_id
            json_dic['info'] = "端口扫描开启成功"
            json_dic['flag'] = 1
            return HttpResponse("<script>parent.domain_brute_form_result('" + json.dumps(json_dic) + "');</script>")
        except Exception as e:
            print e
            json_dic['info'] = "端口扫描开启失败"
            json_dic['flag'] = 0
            return HttpResponse("<script>parent.domain_brute_form_result('" + json.dumps(json_dic) + "');</script>")
    return render(request, 'tools/domain_brute.html')


def view_web_spider(request, id):
    if not auth(request):
        return HttpResponseRedirect('/user/login/')
    args = {}
    try:
        web_spider = models.Spider.objects.get(id=id)
    except Exception as e:
        print e
        args['flag'] = 0
        args['info'] = "没有找到该任务"
        # HttpResponse('<script>form_result("请等待目前任务执行完成");</script>')
    else:
        domain = web_spider.target_domain
        url_objs = models.Url.objects.filter(domain=domain)
        if web_spider.status != 2:
            args['flag'] = 1
            args['info'] = "扫描未完成，请耐心等待"
        else:
            args['info'] = 'web爬虫扫描完成'
            args['flag'] = 2
            args['id'] = 0
        urls = []
        args['num'] = len(url_objs)
        for url_obj in url_objs:
            domain = url_obj.domain
            url = url_obj.url
            urls.append(url)
        tree_obj = Tree(domain, urls)
        tree = tree_obj.make_tree()
        args['tree'] = tree
    return JsonResponse(json.dumps(args), safe=False)
    # return render(request, 'tools/web_spider.html')


def web_spider(request):
    if not auth(request):
        return HttpResponseRedirect('/user/login/')
    flag = auth_power(request.user, 'spider')
    if not flag:
        return HttpResponse('<script>alert("你没有该操作的权限")</script>')
    if request.method == 'GET':
        return render(request, 'tools/web_spider.html')
    elif request.method == 'POST':
        params = request.POST
        # 开启新web爬虫任务
        json_dic = {}
        try:
            if 'id' in params and int(params['id']) != 0:
                id = int(params['id'])
                domain_brute_obj = models.Spider.objects.get(id=id)
                if domain_brute_obj.status != 2:
                    json_dic['flag'] = 0
                    json_dic['info'] = "请等待目前任务执行完成"
                    HttpResponse("<script>parent.web_spider_form_result('" + json.dumps(json_dic) + "');</script>")
                    # elif domain_brute_obj.status == 2:
                    #     return render(request, "tools/domain_brute.html")
            if 'url' not in params:
                return HttpResponse("<script>parent.show_error('请输入目标网址');</script>")
                # 开启新端口扫描任务
            url = params['url']
            domain = get_domain(url)
            web_spider_objs = models.Spider.objects.filter(target_domain=domain)
            if not web_spider_objs:
                args = {}
                user_setting = UserSetting.objects.get(user=request.user)
                # args['spider_model'] = "usually"  # all usually
                args['spider_thread'] = user_setting.spider_thread # SPIDER_THREAD
                spider_obj = Spider(target_domain=domain, target_url=url, thread=args['spider_thread'])
                spider_obj.save()
                spider_obj_id = spider_obj.id
                args['spider_id'] = spider_obj.id
                args['domain'] = domain
                args['target_url'] = url
                args['model'] = 13
                json_args = json.dumps(args)
                json_args = json_args.replace('"', "'")
                work = 'python ' + TOOLS_PATH + os.sep + 'core.py ' + json_args
                p = subprocess.Popen(work)
                print 'open success:', p
            else:
                if web_spider_objs[0].status == 2:
                    domain = web_spider_objs[0].target_domain
                    url_objs = models.Url.objects.filter(domain=domain)
                    urls = []
                    for url_obj in url_objs:
                        domain = url_obj.domain
                        url = url_obj.url
                        urls.append(url)
                    tree_obj = Tree(domain, urls)
                    tree = tree_obj.make_tree()
                    json_dic['flag'] = 2
                    json_dic['id'] = 0
                    json_dic['info'] = 'web爬虫扫描完成'
                    json_dic['tree'] = tree
                    json_dic['num'] = len(url_objs)
                    return HttpResponse("<script>parent.web_spider_form_result('" + json.dumps(json_dic) + "');</script>")
                else:
                    spider_obj_id = web_spider_objs[0].id
            json_dic['id'] = spider_obj_id
            json_dic['info'] = "端口扫描开启成功"
            json_dic['flag'] = 1
            return HttpResponse("<script>parent.web_spider_form_result('" + json.dumps(json_dic) + "');</script>")
        except Exception as e:
            print e
            json_dic['info'] = "端口扫描开启失败"
            json_dic['flag'] = 0
            return HttpResponse("<script>parent.web_spider_form_result('" + json.dumps(json_dic) + "');</script>")


# def exploit_attack(request):
#     return render(request, 'tools/exploit_attack.html')
    # return HttpResponse("poc")


# def fuzz(request):
#     return HttpResponse("fuzz")


# http://v3.bootcss.com/examples/theme/#
# http://v3.bootcss.com/components/
# http://www.bootcss.com/
# http://v3.bootcss.com/examples/dashboard/


