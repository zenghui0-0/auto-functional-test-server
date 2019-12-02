"""
Autor:Zeng Hui
Date: 11/11/2019
mail: zenghui0_0@163.com
"""
from django.shortcuts import render
from django.shortcuts import redirect
from . import models, forms
import hashlib

# Create your views here.

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
    return render(request, 'index/tasks.html', locals())


def addTasks(request):
    if not request.session.get('is_login', None):
        return redirect('/login/', locals())
    return render(request, 'index/addTasks.html', locals())


def devices(request):
    if not request.session.get('is_login', None):
        return redirect('/login/', locals())
    devices = models.myDevice.objects.all()#.all equals select *
    return render(request, 'index/devices.html', locals())

def addDevices(request):
    if not request.session.get('is_login', None):
        return redirect('/login/', locals())
    devices = models.myDevice.objects.all()#.all equals select *
    if request.method == 'POST':
        device_form = forms.DevicesForm(request.POST)
        message = 'please check input content!'
        if device_form.is_valid():
            host_name = device_form.cleaned_data.get('host_name')
            DUT_IP = device_form.cleaned_data.get('DUT_IP')
            HDT_IP = device_form.cleaned_data.get('HDT_IP')
            tag = device_form.cleaned_data.get('tag')
            email = device_form.cleaned_data.get('email')

            #adding device into db
            new_device = models.myDevice()
            new_device.host_name = host_name
            new_device.HDT_IP = HDT_IP
            new_device.DUT_IP = DUT_IP
            new_device.tag = tag
            new_device.email = email
        else:
            return render(request, 'login/login.html', locals())
    return render(request, 'index/addDevices.html', locals())

def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = 'please check input content!'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = models.User.objects.get(name=username)
            except:
                message = 'username not exist!'
                return render(request, 'login/login.html', locals())

            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = 'incorrect password!'
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
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = 'username already exists'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = 'email address been used'
                    return render(request, 'login/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                #new_user.sex = sex
                new_user.save()
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