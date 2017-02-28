# coding=utf-8
import json

from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, render_to_response
# from django.template import RequestContext
# from django.shortcuts import render_to_response
# Create your views here.
# from model.models import User, SwordUser
# import model.dir.EmailToken
from HeavenSword.settings import DEFAULT_FROM_EMAIL, EMAIL_HOST_USER
from model.dir.EmailToken import EmailToken
from model.msetting import DOMAIN


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
                response = HttpResponseRedirect('/index/')
                response.set_cookie('username', username, max_age=None)
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
            '/'.join([DOMAIN, 'account/activate', token])
        ])
        from_email = EMAIL_HOST_USER
        send_mail(u'注册用户验证信息', message, from_email, [email])
        user.save()
        return HttpResponse('<script>parent.register_success();</script>')
        # return HttpResponse("<script>parent.register_success();</script>")


def user_activate(request, token):
    token_confirm = EmailToken('xqlpniip)kgj&dod5e=k95!q6su!m$tsy__&li3-vx)tflp#yr')
    username = token_confirm.confirm_validate_token(token)
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


def new_single_task(request):
    if not request.user.is_authenticated():
        return HttpResponse("<div style='text-align:center;margin-top:20%'><h3>请登录</h3><br><br><a href='/user/login/'>点击跳转到登陆页面</a>")
    if request.method == 'GET':
        return render(request, 'task/new_single_task.html')
    if request.method == 'POST':
        params = request.POST
        target = params['target']
        finger_flag = params['finger_flag']
        port_scan_flag = params['port_scan_flag']
        domain_brute_flag = params['domain_brute_flag']
        spider_flag = params['spider_flag']
        exploit_attack_flag = params['exploit_flag']
        port_scan_thread = params['port_scan_thread']
        port_scan_model = params['port_scan_model']
        domain_brute_thread = params['domain_brute_thread']
        spider_thread = params['spider_thread']
        print params
        return render(request, 'task/new_single_task.html')



def new_batch_task(request):
    return render(request, 'task/new_batch_task.html')


def task_list(request):
    return render(request, 'task/task_list.html')


def show_task(request):
    return render(request, 'task/show_task.html')


def task_info(request):
    return render(request, 'task/task_info.html')


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


def one(request):
    return render(request, '1.html')

# http://v3.bootcss.com/examples/theme/#
# http://v3.bootcss.com/components/
# http://www.bootcss.com/
# http://v3.bootcss.com/examples/dashboard/


def view_all_task(request):
    return render(request, 'task/view_all_task.html')


def view_single_task(request):
    return render(request, 'task/view_single_task.html')


def view_batch_task(request):
    return render(request, 'task/view_batch_task.html')