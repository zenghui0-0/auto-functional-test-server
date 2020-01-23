from django.contrib import admin
from TestModel.models import myDevice, Task, User

# Register your models here.
admin.site.site_header = 'WELLCOME'
admin.site.site_title = 'WELLCOME'

class devicesDisplay(admin.ModelAdmin):
    list_display = ('host_name', 'tag') # list

admin.site.register([Task, User])
admin.site.register(myDevice, devicesDisplay)