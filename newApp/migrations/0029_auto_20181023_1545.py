# Generated by Django 2.1.2 on 2018-10-23 12:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newApp', '0028_auto_20181023_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 26, 15, 45, 14, 253621)),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='language',
            field=models.SlugField(default='en', max_length=100),
        ),
    ]