from django.contrib import admin
from TestModel.models import myDevice, Task

# Register your models here.
admin.site.site_header = 'WELLCOME'
admin.site.site_title = 'WELLCOME'

class devicesDisplay(admin.ModelAdmin):
    list_display = ('host_name', 'tag') # list

class tasksDisplay(admin.ModelAdmin):
    list_display = ('id', 'name', 'progress', 'Owner', 'tag', 'status', 'm_time') # list

admin.site.register(myDevice, devicesDisplay)
admin.site.register(Task, tasksDisplay)