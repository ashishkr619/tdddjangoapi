# Generated by Django 3.0.8 on 2020-07-24 15:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='category', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Title', max_length=30)),
                ('body', models.TextField(default='New body', max_length=300)),
                ('summary', models.CharField(default='Summary', max_length=60)),
                ('category', models.ManyToManyField(related_name='category', to='api.Category')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
