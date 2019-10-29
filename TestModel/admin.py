from django.contrib import admin
from TestModel.models import myDevice, Task

# Register your models here.
admin.site.register([Task, myDevice])