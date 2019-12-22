from django.shortcuts import render
from django.shortcuts import redirect
import json
from . import models, forms


def tasks(request):
    tasks = models.Task.objects.exclude(status=4).order_by("-m_time").all().values()#.all equals select *
    return tasks


def startTask(request):
    device_id = request.GET.get("id")
    #add devices
    if not request.session.has_key('device_id'):
        request.session['device_id'] = None
    if device_id:
        request.session['device_id'] = device_id
    else:
        device_id = request.session.get('device_id')
    devices = models.myDevice.objects.filter(id = request.session['device_id']).values('DUT_IP', 'HDT_IP', 'host_name', 'tag', 'status')
    return list(devices)

def deleDevice(request):
    del request.session['device_id']
    return True
    