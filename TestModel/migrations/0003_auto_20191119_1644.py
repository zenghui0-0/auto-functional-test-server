# Generated by Django 2.2.7 on 2019-11-19 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestModel', '0002_auto_20191119_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='mydevice',
            name='m_time',
            field=models.DateTimeField(auto_now=True, verbose_name='update time'),
        ),
        migrations.AddField(
            model_name='mydevice',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'online'), (1, 'offline'), (2, 'unknow'), (3, 'broken'), (4, 'busy')], default=0, verbose_name='device status'),
        ),
        migrations.AlterField(
            model_name='mydevice',
            name='tag',
            field=models.SlugField(blank=True, help_text='For example: John_3dmark_11_12', max_length=100, null=True),
        ),
    ]
