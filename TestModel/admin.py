from django.contrib import admin
from TestModel.models import myDevice, Task

# Register your models here.
admin.site.site_header = 'WELLCOME'
admin.site.site_title = 'WELLCOME'

class devicesDisplay(admin.ModelAdmin):
    list_display = ('HDT_IP', 'tag') # list

admin.site.register(Task)
admin.site.register(myDevice, devicesDisplay)