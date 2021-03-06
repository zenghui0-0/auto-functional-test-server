﻿import djcelery
import datetime

djcelery.setup_loader()

CELERY_TIMEZONE = 'Asia/Shanghai'
BROKER_URL = 'redis://localhost:6379' #clery4 版本用来代替CELERY_BROKER_URL
CELERY_BROKER_URL = 'redis://localhost:6379/1'
#CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'

#需执行异步的子应用
CELERY_IMPORTS = (
    'TestModel.tasks',
)

# celery内容等消息的格式设置
CELERY_ACCEPT_CONTENT = ['application/json', ]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# django setting.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}
# 为定时任务和异步任务单独设置QUEUES
CELERY_QUEUES = {
    'beat_tasks': {
        'exchange': 'beat_tasks',
        'exchange_type': 'direct',
        'binding_key': 'beat_tasks'
    },
    'work_queue': {
        'exchange': 'work_queue',
        'exchange_type': 'direct',
        'binding_key': 'work_queue'
    }
}

# 默认使用队列
CELERY_DEFAULT_QUEUE = 'work_queue'

# 某个程序中出现的队列，在broker中不存在，则立刻创建它
CELERY_CREATE_MISSING_QUEUES = True

CELERYD_PREFETCH_MULTIPLIER = 1

#  有些情况下可以防止死锁
CELERYD_FORCE_EXECV = True

#  设置并发的worker数量
CELERYD_CONCURRENCY = 4

# 允许重试
CELERY_ACKS_LATE = True

#  每个worker最多执行100个任务被销毁，可以防止内存泄漏
CELERYD_MAX_TASKS_PER_CHILD = 100

#  单个任务的最大运行时间，超过就杀死
CELERYD_TASK_TIME_LEMIT = 12 * 60

#  定时任务
CELERYBEAT_SCHEDULE = {
    'task1': {
        'task': 'course-task',
        'schedule': datetime.timedelta(seconds=5),  # 每5秒执行一次
        'options': {
            'queue': 'beat_tasks'  # 当前定时任务是跑在beat_tasks队列上的
        }
    }
}
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/
