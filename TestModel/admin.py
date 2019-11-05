from django.contrib import admin
from TestModel.models import myDevice, Task

# Register your models here.
admin.site.site_header = 'WELLCOME'
admin.site.site_title = 'WELLCOME'

admin.site.register([Task, myDevice])