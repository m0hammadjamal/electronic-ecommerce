# Generated by Django 5.1.1 on 2025-01-03 15:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_datetime', models.DateTimeField(auto_now=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_datetime', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(limit_choices_to={'is_manager': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'manager',
                'verbose_name_plural': 'managers',
                'db_table': 'managers_manager',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'notification',
                'verbose_name_plural': 'notifications',
                'db_table': 'notification_table',
                'ordering': ['-id'],
            },
        ),
    ]
