# Generated by Django 2.1.2 on 2018-10-23 13:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newApp', '0029_auto_20181023_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 26, 16, 4, 53, 695155)),
        ),
    ]
