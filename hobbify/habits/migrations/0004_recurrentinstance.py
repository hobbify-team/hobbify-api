# Generated by Django 3.0.8 on 2020-07-10 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0003_delete_recurrentinstance'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecurrentInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created.', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date time on which the object was last modified.', verbose_name='modified at')),
                ('is_hidden', models.BooleanField(default=False, help_text='Due to system requirements a database entry cannot be deleted. Hidden represents deleted for the users.', verbose_name='hidden')),
                ('rule', models.CharField(max_length=200, null=True)),
                ('recurrence', models.CharField(max_length=200, null=True)),
                ('done', models.BooleanField(default=False, help_text='Used for disabling the habit or marking it as finished.', verbose_name='done habit status')),
                ('habit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='habits.Habit')),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
    ]
