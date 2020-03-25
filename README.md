# auto functional test server
[INSTALLED APPS]
1, python modules should be installed: django, mysqlclient, redis, celery, django-celery, django_celery_results, flower;
2, data base: redis, mysql should installed and start first;

[START APPS]
celery -A AutoTestServer worker --pool=solo -l info --concurrency=10
celery worker -A AutoTestServer -l debug
python manage.py runserver