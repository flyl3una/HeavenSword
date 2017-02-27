# coding=utf-8
import json

from django.contrib.auth import authenticate, logout
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
# from django.template import RequestContext
# from django.shortcuts import render_to_response
# Create your views here.
# from model.models import User, SwordUser


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    if request.method == 'POST':
        url = request.POST.get('target')
        print url
    # return render_to_response('index.html', {"key":"value"})


def login(request):
    if request.user.is_authenticated():
        return HttpResponse("""您已经登陆!<br/><a href="/index/">点击跳转到主页</a>""")
    if request.method == 'GET':
        return render(request, 'login1.html')
    if request.method == 'POST':
        # username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        print email, password
        if user:
            if user.is_active:
                login(request, user)
                response = HttpResponseRedirect('/index/')
                response.set_cookie('email', email, max_age=None)
                return response
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(email, password)
            return HttpResponse("Invalid login details supplied.")


def logoutView(request):
    logout(request)
    # return render(request, '/')
    return HttpResponseRedirect('/')


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        params = request.POST
        email = params['email']
        password = params['password']
        password2 = params['password2']
        username = params['username']
        if password != password2:
            # result={}
            # result['status'] = 0
            # result['error'] = '两次输入密码不相同，请重新输入。'
            return HttpResponse("<script>parent.register_error1();</script>")
        else:
            return HttpResponse("<script>parent.register_success();</script>")


def help(request):
    return render(request, 'help.html')


def batch(request):
    return render(request, 'batch.html')


def operation(request):
    return render(request, 'operation.html')


def new_single_task(request):
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