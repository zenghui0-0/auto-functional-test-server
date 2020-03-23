# auto functional test server
[INSTALLED APPS]
1, python modules should be installed: django, celery, djcelery, flower;
2, data base: redis, mysql should installed and start first;

[START APPS]
celery -A AutoTestServer worker --pool=solo -l info
python manage.py runserver