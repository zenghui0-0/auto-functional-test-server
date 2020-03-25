from django.shortcuts import render
from django.shortcuts import redirect
from django_celery_results.models import TaskResult
import json
from . import models, forms


def tasks(request):
    results = TaskResult.objects.all().values()
    print(results)
    tasks = models.Task.objects.exclude(status=4).order_by("-m_time").all().values()#.all equals select *
    return tasks


def deleDevice(request):
    try:
        del request.session['device_id']
    except Exception as e:
        print(e)
    return True
    