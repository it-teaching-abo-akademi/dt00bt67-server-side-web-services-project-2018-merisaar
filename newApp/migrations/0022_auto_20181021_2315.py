# Generated by Django 2.1.2 on 2018-10-21 20:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newApp', '0021_auto_20181021_2259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 24, 23, 15, 44, 279879)),
        ),
    ]