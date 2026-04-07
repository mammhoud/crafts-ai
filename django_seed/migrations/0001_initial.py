# Generated migration for email automation models

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('recipient', models.EmailField(db_index=True, max_length=254)),
                ('subject', models.CharField(max_length=255)),
                ('status', models.CharField(
                    choices=[
                        ('queued', 'Queued'),
                        ('sending', 'Sending'),
                        ('sent', 'Sent'),
                        ('failed', 'Failed'),
                        ('bounced', 'Bounced')
                    ],
                    db_index=True,
                    default='queued',
                    max_length=20
                )),
                ('template_used', models.CharField(blank=True, max_length=255)),
                ('message_body', models.TextField(blank=True)),
                ('error_message', models.TextField(blank=True)),
                ('retry_count', models.PositiveIntegerField(default=0)),
                ('last_retry_at', models.DateTimeField(blank=True, null=True)),
                ('group_name', models.CharField(blank=True, max_length=100)),
                ('task_id', models.CharField(blank=True, db_index=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sent_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='email_logs',
                    to=settings.AUTH_USER_MODEL
                )),
            ],
            options={
                'db_table': 'email_log',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('users', models.ManyToManyField(related_name='email_groups', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_group',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(
                    choices=[
                        ('supervisor', 'Supervisor'),
                        ('manager', 'Manager'),
                        ('instructor', 'Instructor'),
                        ('content_manager', 'Content Manager')
                    ],
                    db_index=True,
                    max_length=50
                )),
                ('assigned_at', models.DateTimeField(auto_now_add=True)),
                ('assigned_by', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='assigned_roles',
                    to=settings.AUTH_USER_MODEL
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='roles',
                    to=settings.AUTH_USER_MODEL
                )),
            ],
            options={
                'db_table': 'user_role',
                'ordering': ['user', '-role'],
            },
        ),
        migrations.AddIndex(
            model_name='emaillog',
            index=models.Index(fields=['status', 'timestamp'], name='email_log_status_c8e8e5_idx'),
        ),
        migrations.AddIndex(
            model_name='emaillog',
            index=models.Index(fields=['recipient', 'timestamp'], name='email_log_recipie_8f9a3c_idx'),
        ),
        migrations.AddIndex(
            model_name='emaillog',
            index=models.Index(fields=['task_id'], name='email_log_task_id_4a5b2d_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='userrole',
            unique_together={('user', 'role')},
        ),
    ]
