F"""
Autor:Zeng Hui
Date: 11/11/2019
mail: zenghui0_0@163.com
"""
import sys
import time
import datetime
import hashlib
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib  import  auth
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from . import models, forms
from . import taskViews
from .tasks import *
from AutoTestServer.celery import app

# Create your views here.
def CMD(request):
    if not request.session.get('is_login', None):
        return redirect('/login/', locals())
    user = request.session.get('user_name')
    res = coplyent_execute_cmd.delay("IPCONFIG_TESTS", **{'cmd' : "ipconfig", 'run_time' : 1, 'dut_ip' : "192.101.16.228", 'port' : 9922}) 
    task_id = res.task_id
    #print(task_id)
    new_task = models.Task()
    new_task.name = task_id
    new_task.Owner = user
    new_task.tag = res.name
    new_task.status = res.status
    new_task.m_time = res.date_created
    new_task.progress = 0
    new_task.save()
    p = 0
    while not res.ready():
        new_task.status = res.status
        result = res.result
        if res.state == 'PROGRESS':    
            try:
                p = result.get('p')
            except Exception as e:
                pass
        new_task.progress = p
        new_task.save()
        time.sleep(1)

    return HttpResponse(res.task_id)


def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/', locals())
    Dir = dir()
    return render(request, 'index/index.html', locals())


def tasks(request):
    if not request.session.get('is_login', None):
        return redirect('/login/', locals())
    all_tasks = taskViews.tasks(request)
    return render(request, 'index/tasks.html', locals())


def startTask(request):
    if not request.session.get('is_login', None):
        return redirect('/login/', locals())
    id = request.GET.get("id")
    if id:
        request.session['device_id'] = id
        request.session['device_add_time'] = datetime.datetime.now().strftime("%H:%M:%S %p")
    device_id = request.session.get('device_id', None)
    device_add_time = request.session.get('device_add_time', '0:00')
    device = models.myDevice.objects.values().filter(id=device_id).first()
    device_form = forms.DevicesForm()
    if request.method == 'POST':
        device_form = forms.DevicesForm(request.POST)
        message = 'please check input content!'
        if device_form.is_valid():
            host_name = device_form.cleaned_data.get('host_name')
            DUT_IP = device_form.cleaned_data.get('DUT_IP')
            HDT_IP = device_form.cleaned_data.get('HDT_IP')
            tag = device_form.cleaned_data.get('tag')
            email = device_form.cleaned_data.get('email')
            status = device_form.cleaned_data.get('status')

            #updating device info
            if not id: #add a new device
                new_device = models.myDevice()
            else: #update old device info
                new_device = models.myDevice.objects.get(id=id)
            new_device.host_name = host_name
            new_device.HDT_IP = HDT_IP
            new_device.DUT_IP = DUT_IP
            new_device.tag = tag
            new_device.email = email
            new_device.status = status
            new_device.Owner = request.session['user_name']
            new_device.done = True
            new_device.save()

            #return redirect('index/startTask.html')
        else:
            return render(request, 'index/startTask.html', locals())   
    else:
        device_form = forms.DevicesForm(initial=device)
        return render(request, 'index/startTask.html', locals())
    return render(request, 'index/startTask.html', locals())


def startTaskDeleDevices(request):
    taskViews.deleDevice(request)
    return render(request, 'index/startTask.html', locals())


def devices(request):
    if not request.session.get('is_login', None):
        return redirect('/login/', locals())
    user = request.session.get('user_name')
    devices = models.myDevice.objects.order_by("-m_time").filter(Owner=user).values()#.all equals select *
    return render(request, 'index/devices.html', locals())


def addDevice(request):
    if not request.session.get('is_login', None):
        return redirect('/login/', locals())
    id = request.GET.get("id")
    device = models.myDevice.objects.values().filter(id=id).first()
    device_form = forms.DevicesForm()
    if request.method == 'POST':
        device_form = forms.DevicesForm(request.POST)
        message = 'please check input content!'
        if device_form.is_valid():
            host_name = device_form.cleaned_data.get('host_name')
            DUT_IP = device_form.cleaned_data.get('DUT_IP')
            HDT_IP = device_form.cleaned_data.get('HDT_IP')
            tag = device_form.cleaned_data.get('tag')
            email = device_form.cleaned_data.get('email')
            status = device_form.cleaned_data.get('status')

            #updating device info
            if not id: #add a new device
                new_device = models.myDevice()
            else: #update old device info
                new_device = models.myDevice.objects.get(id=id)
            new_device.host_name = host_name
            new_device.HDT_IP = HDT_IP
            new_device.DUT_IP = DUT_IP
            new_device.tag = tag
            new_device.email = email
            new_device.status = status
            new_device.Owner = request.session['user_name']
            new_device.done = True
            new_device.save()

            return redirect('/devices/')
        else:
            return render(request, 'index/addDevice.html', locals())   
    else:
        device_form = forms.DevicesForm(initial=device)
        return render(request, 'index/addDevice.html', locals())
    return render(request, 'index/addDevice.html', locals())


def deleDevice(request):
    id = request.GET.get("id")
    models.myDevice.objects.filter(id = id).delete()
    return redirect('/devices/')


def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = 'please check input content!'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user_obj = auth.authenticate(username=username, password=password)

            if user_obj:
                auth.login(request, user_obj)
                request.session['is_login'] = True
                #request.session['user_id'] = user
                request.session['user_name'] = username
                return redirect('/index/')
            else:
                message = 'incorrect password or user name!'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "please check your inputs"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            #sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = 'please enter same password'
                return render(request, 'login/register.html', locals())
            if User.objects.filter(username=username).exists():
                message = 'username already exists'
                return render(request, 'login/register.html', locals())
            else:
                new_obj = User.objects.create_user(username=username, password=password1, email=email)
                return redirect('/login/')
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login/")