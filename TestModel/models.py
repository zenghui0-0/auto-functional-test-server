# models.py
from django.db import models
 
class User(models.Model):

    """
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    """
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    #sex = models.CharField(max_length=32, choices=gender, default="男")
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "Users"
        verbose_name_plural = "Users"

class myDevice(models.Model):
    DUT_IP    = models.GenericIPAddressField()
    HDT_IP    = models.GenericIPAddressField()
    user_name = models.SlugField()
    password  = models.SlugField()
    tag       = models.SlugField(max_length=100, null=True, blank=True)
    email     = models.EmailField(max_length=100, null=True, blank=True, verbose_name='email_address', help_text='email address')
    def __str__(self):
        return self.HDT_IP

    class Meta:
        verbose_name = "Devices"
        verbose_name_plural = "Devices"

class Task(models.Model):
    name = models.CharField(max_length=20)