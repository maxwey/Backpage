# Generated by Django 3.0.8 on 2020-08-04 03:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParentPost',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='feed.Post')),
            ],
            bases=('feed.post',),
        ),
        migrations.CreateModel(
            name='CommentPost',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='feed.Post')),
                ('parent_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='comment_parent_post', to='feed.Post')),
            ],
            bases=('feed.post',),
        ),
    ]
