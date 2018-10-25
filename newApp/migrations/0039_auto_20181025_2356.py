# Generated by Django 2.1.2 on 2018-10-25 20:56

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newApp', '0038_auto_20181025_0317'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='auction',
            options={'ordering': ['deadline']},
        ),
        migrations.AlterField(
            model_name='auction',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 28, 23, 56, 23, 860889)),
        ),
        migrations.AlterField(
            model_name='bidauction',
            name='auction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='auctionBid', to='newApp.Auction'),
        ),
    ]
