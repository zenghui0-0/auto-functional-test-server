from __future__ import absolute_import, unicode_literals
import time, random
from celery import task
from celery import shared_task
from django.core.mail import send_mail
from django.http import HttpResponse

#定义异步写文件方法
@task
def file_task():
        #写文件操作  文件对象
        file_object = open("./data.text",'a+',encoding='utf-8')
        file_object.write("hello")
        file_object.close()
        print("ok")

#定义异步发邮件的方法
@task
def email_():
        captcha_text = []
        DEFAULT_FROM_EMAIL = ["AQcenter@amd.com"]
        return "SUCESS!"
        for i in range(4):
        #定义验证码字符
                str = 'qwertyuiopasdfghjklzxcvbnm1234567890'
                c = random.choice(str)
                captcha_text.append(c)
        #返回随机生成的字符串         
        captcha = "".join(captcha_text)
        res = send_mail("欢迎注册",'您的验证码是:'+ captcha,DEFAULT_FROM_EMAIL, ['zenghui0_0@163.com'])
        if res:
                return HttpResponse("发送成功")
        else:
                return HttpResponse("发送失败")

@task
def add(x, y):
    print("{} + {} = {})".format(x,y,x+y))
    return (x + y)