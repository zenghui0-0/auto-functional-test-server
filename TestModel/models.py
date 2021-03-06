# models.py
from django.db import models
 

class myDevice(models.Model):

    asset_status = (
        (0, 'Online'),
        (1, 'Offline'),
        (2, 'Unknow'),
        (3, 'Busy'),
        )

    DUT_IP    = models.GenericIPAddressField()
    HDT_IP    = models.GenericIPAddressField(null=True, blank=True)
    user_name = models.SlugField(max_length=100,null=True, blank=True)
    host_name = models.SlugField(max_length=100, help_text='a uniq name for your dut')
    password  = models.SlugField(max_length=100, null=True, blank=True)
    tag       = models.SlugField(max_length=100, null=True, blank=True, help_text='For example: John_3dmark_11_12')
    email     = models.EmailField(max_length=100, null=True, blank=True, verbose_name='email_address', help_text='email address')
    status    = models.SmallIntegerField(choices=asset_status, default=0, verbose_name='device status')
    Owner     = models.SlugField(max_length=100, default="Admin")
    m_time    = models.DateTimeField(auto_now=True, verbose_name='update time')
    def __str__(self):
        return self.HDT_IP

    class Meta:
        verbose_name = "Devices"
        verbose_name_plural = "Devices"

class Task(models.Model):
    name      = models.CharField(max_length=50, null=True, blank=True)
    progress  = models.PositiveSmallIntegerField(default=0)
    Owner     = models.SlugField(max_length=100, default="Admin")
    tag       = models.SlugField(max_length=100, null=True, blank=True, help_text='For example: John_3dmark_11_12')
    status    = models.SlugField(max_length=100, default="UNKNOWN")
    m_time    = models.DateTimeField(auto_now=False, verbose_name='create time')
