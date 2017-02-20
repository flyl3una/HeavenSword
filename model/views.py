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
    return HttpResponseRedirect('/')


def register(request):
    return render(request, 'register.html')


def batch(request):
    return render(request, 'batch.html')


def operation(request):
    return render(request, 'operation.html')


def one(request):
    return render(request, '1.html')


def finger(request):
    return render(request, 'scan/finger.html', {"test": "test"})
    # return HttpResponse("finger")


def port(request):
    return HttpResponse("port")


def poc(request):
    return HttpResponse("poc")


def spider(request):
    return HttpResponse("spider")


def fuzz(request):
    return HttpResponse("fuzz")


