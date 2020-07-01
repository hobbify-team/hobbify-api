# Generated by Django 3.0.7 on 2020-07-01 01:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created.', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date time on which the object was last modified.', verbose_name='modified at')),
                ('is_hidden', models.BooleanField(default=False, help_text='Due to system requirements a database entry cannot be deleted. Hidden represents deleted for the users.', verbose_name='hidden')),
                ('name', models.CharField(max_length=40)),
                ('description', models.CharField(max_length=150, null=True)),
                ('frequency', models.IntegerField(choices=[(1, 'Daily'), (2, 'Weekly'), (3, 'Montly'), (4, 'Every 3 Days'), (5, 'Weekend')], default=1)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Date time on which the habit is intended to start.', null=True, verbose_name='habit start date')),
                ('end_date', models.DateTimeField(help_text='Date time on which the habit is intended to end.', null=True, verbose_name='habit end date')),
                ('paused', models.BooleanField(default=False, help_text='Used for disabling the habit or marking it as paused.', verbose_name='paused habit status')),
                ('done', models.BooleanField(default=False, help_text='Used for disabling the habit or marking it as finished.', verbose_name='done habit status')),
                ('is_private', models.BooleanField(default=True, help_text='Set to true when the user has set a it as a private habit.', verbose_name='private status')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
    ]
