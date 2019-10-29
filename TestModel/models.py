# models.py
from django.db import models
 
class Test(models.Model):
    name = models.CharField(max_length=20)

class myDevice(models.Model):
    DUT_IP    = models.GenericIPAddressField()
    HDT_IP    = models.GenericIPAddressField()
    user_name = models.SlugField()
    password  = models.SlugField()
    email     = models.EmailField()
    def __unicode__(self):
        return self.HDT_IP

class Task(models.Model):
    name = models.CharField(max_length=20)