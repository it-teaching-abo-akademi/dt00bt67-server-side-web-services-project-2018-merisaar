# Generated by Django 2.1.2 on 2018-10-24 20:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newApp', '0034_auto_20181024_1959'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='currency',
        ),
        migrations.AlterField(
            model_name='auction',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 27, 23, 7, 0, 276813)),
        ),
    ]