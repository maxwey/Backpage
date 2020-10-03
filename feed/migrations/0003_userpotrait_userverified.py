# Generated by Django 3.0.8 on 2020-08-12 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_commentpost_parentpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='portrait',
            field=models.ImageField(blank=True, null=True, upload_to='portraits'),
        ),
    ]