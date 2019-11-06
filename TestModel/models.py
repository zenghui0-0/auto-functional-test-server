# models.py
from django.db import models
 
class Test(models.Model):
    name = models.CharField(max_length=20)

class myDevice(models.Model):
    DUT_IP    = models.GenericIPAddressField()
    HDT_IP    = models.GenericIPAddressField()
    user_name = models.SlugField()
    password  = models.SlugField()
    tag       = models.SlugField(max_length=100, null=True, blank=True)
    email     = models.EmailField(max_length=100, null=True, blank=True, verbose_name='email_address', help_text='email address')
    def __str__(self):
        return self.HDT_IP

class Task(models.Model):
    name = models.CharField(max_length=20)