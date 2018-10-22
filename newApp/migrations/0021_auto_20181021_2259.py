# Generated by Django 2.1.2 on 2018-10-21 19:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newApp', '0020_auto_20181021_2221'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidauction',
            name='email_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bidauction',
            name='email_sent_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='auction',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 24, 22, 59, 6, 550620)),
        ),
    ]