# coding=utf-8
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
# from django.template import RequestContext
# from django.shortcuts import render_to_response
# Create your views here.


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    if request.method == 'POST':
        url = request.POST.get('target')
        print url
    # return render_to_response('index.html', {"key":"value"})


def login(request):
    return render(render, 'login.html')


def logout(request):
    return render(request, '/')
    # return HttpResponseRedirect('/')


def register(request):
    return render(request, 'register.html')


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