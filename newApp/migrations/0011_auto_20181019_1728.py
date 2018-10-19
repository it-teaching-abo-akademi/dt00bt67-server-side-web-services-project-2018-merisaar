# Generated by Django 2.1.2 on 2018-10-19 14:28

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newApp', '0010_auto_20181019_1701'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='highestBid',
        ),
        migrations.AddField(
            model_name='bidauction',
            name='auction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bidder', to='newApp.Auction'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 22, 17, 28, 57, 909616)),
        ),
        migrations.AlterField(
            model_name='bidauction',
            name='bidder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bidauction',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 19, 17, 28, 57, 909616)),
        ),
    ]
