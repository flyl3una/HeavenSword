# coding=utf-8
from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'index.html')


def login(request):
    return render(render, 'login.html')


def register(request):
    return render(request, 'register.html')


def batch(request):
    return render(request, 'batch.html')
