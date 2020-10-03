# Generated by Django 3.0.8 on 2020-08-16 00:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0004_realuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realuser',
            name='expiration_time',
            field=models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0), null=True),
        ),
        migrations.AlterField(
            model_name='realuser',
            name='session_id',
            field=models.CharField(max_length=128, null=True),
        ),
    ]