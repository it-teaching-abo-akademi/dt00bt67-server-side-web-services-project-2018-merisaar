# Generated by Django 2.1.2 on 2018-10-21 19:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newApp', '0019_auto_20181021_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 24, 22, 21, 23, 814741)),
        ),
    ]
