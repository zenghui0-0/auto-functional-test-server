from django.shortcuts import render
from django.shortcuts import redirect
from django_celery_results.models import TaskResult
import json
from . import models, forms


def tasks(request):
    results = TaskResult.objects.all().values()
    
    for result in results:
        if not result:
            continue
        task_id = result.get('task_id')
        status  = result.get('status')
        if models.Task.objects.filter(name=task_id).exists():
            new_task = models.Task.objects.get(name=task_id)
        else:
            new_task = models.Task()
        new_task.name = task_id
        new_task.tag = result.get('task_name')
        new_task.status = status
        new_task.m_time = result.get('date_created')
        p = 0
        if status == "PROGRESS":
            try:
                p = eval(result.get('result')).get('p')
            except Exception as e:
                print(e)
            new_task.progress = p
        elif status == "SUCCESS":
            new_task.progress = 100
        elif status == "FAILURE":
            new_task.progress = 99
        else:
            new_task.progress = 1
        new_task.save()
    """
        p=result.get('result')
        print(p)
        print(type(p))
        #print(type(result))

    {'id': 3, 'task_id': 'a7acc170-4974-4fef-8714-0dae2490f980', 'task_name': 'TestModel.tasks.email_', 'task_args': '()', 'task_kwargs': '{}', 'status': 'FAILURE', 'worker': 'celery@SHA-L-HUI2ZENG2', 'content_type': 'application/json', 'content_encoding': 'utf-8', 'result': '{"exc_type": "ValueError", "exc_message": ["not enough values to unpack (expected 3, got 0)"], "exc_module": "builtins"}', 'date_created': datetime.datetime(2020, 3, 24, 6, 33, 55, 893856, tzinfo=<UTC>), 'date_done': datetime.datetime(2020, 3, 24, 6, 33, 55, 893856, tzinfo=<UTC>), 'traceback': None, 'meta': '{"children": []}'}
    """
    all_tasks = models.Task.objects.all() 
    return all_tasks

def deleDevice(request):
    try:
        del request.session['device_id']
    except Exception as e:
        print(e)
    return True
