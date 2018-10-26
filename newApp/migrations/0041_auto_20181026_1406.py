# Generated by Django 2.1.2 on 2018-10-26 11:06

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newApp', '0040_auto_20181026_0156'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('body', models.TextField()),
                ('title', models.CharField(max_length=150)),
                ('emailTo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emailTo', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='auction',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 29, 14, 6, 33, 356643)),
        ),
    ]