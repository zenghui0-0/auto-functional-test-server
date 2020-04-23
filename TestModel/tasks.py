from __future__ import absolute_import, unicode_literals
import time, random
from celery import task
from celery import shared_task
from django.core.mail import send_mail
from django.http import HttpResponse
from TestSuites.conplyent_connect_execute import RUN
from . import models, forms


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

@task(bind=True)
def coplyent_execute_cmd(self, test_name, **kwargs):
    {'cmd' : "ipconfig", 'run_time' : 1, 'dut_ip' : "192.101.16.228", 'port' : 9922}
    cmd = kwargs.get('cmd')
    run_time = kwargs.get('run_time')
    dut_ip = kwargs.get('dut_ip')
    port = kwargs.get('port')
    self.update_state(state="PROGRESS", meta={'p': 1})
    time.sleep(10)
    self.update_state(state="PROGRESS", meta={'p': 33})
    test1 = RUN(dut_ip, port, test_name)
    test1.start_test("ipconfig", 0.1,)
    self.update_state(state="PROGRESS", meta={'p': 66})
    time.sleep(10)
    self.update_state(state="PROGRESS", meta={'p': 99})
    return True


@task
def execute():
    pass

