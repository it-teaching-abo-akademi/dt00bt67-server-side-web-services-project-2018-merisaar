# Generated by Django 2.1.2 on 2018-10-21 16:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newApp', '0014_auto_20181021_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 24, 19, 43, 23, 39920)),
        ),
    ]