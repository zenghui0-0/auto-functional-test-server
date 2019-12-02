# Generated by Django 2.2.7 on 2019-11-29 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestModel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mydevice',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'Online'), (1, 'Offline'), (2, 'Unknow'), (3, 'Busy')], default=0, verbose_name='device status'),
        ),
    ]
