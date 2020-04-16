from django.shortcuts import render
from django.shortcuts import redirect
from django_celery_results.models import TaskResult
import json
from . import models, forms


def tasks(request):
    results = TaskResult.objects.all().values()
    new_task = models.Task()
    for result in results:
        #new_task.
        if not result:
            continue
        print(result)
        print(type(result))
    """
    {'id': 3, 'task_id': 'a7acc170-4974-4fef-8714-0dae2490f980', 'task_name': 'TestModel.tasks.email_', 'task_args': '()', 'task_kwargs': '{}', 'status': 'FAILURE', 'worker': 'celery@SHA-L-HUI2ZENG2', 'content_type': 'application/json', 'content_encoding': 'utf-8', 'result': '{"exc_type": "ValueError", "exc_message": ["not enough values to unpack (expected 3, got 0)"], "exc_module": "builtins"}', 'date_created': datetime.datetime(2020, 3, 24, 6, 33, 55, 893856, tzinfo=<UTC>), 'date_done': datetime.datetime(2020, 3, 24, 6, 33, 55, 893856, tzinfo=<UTC>), 'traceback': None, 'meta': '{"children": []}'}
    """
    #new_task.save()
    
    #tasks = models.Task.objects.exclude(status=4).order_by("-m_time").all().values()#.all equals select *
    #return tasks
    return results

def deleDevice(request):
    try:
        del request.session['device_id']
    except Exception as e:
        print(e)
    return True
    