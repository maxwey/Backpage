# Generated by Django 3.0.8 on 2020-09-01 02:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0005_make_realuser_fields_nullable'),
    ]

    operations = [
        migrations.AddField(
            model_name='realuser',
            name='track_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='realuser',
            name='session_id',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='intro_text',
            field=models.TextField(blank=True),
        ),
        migrations.CreateModel(
            name='PostInteractionTracker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=32)),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.RealUser')),
            ],
        ),
    ]
