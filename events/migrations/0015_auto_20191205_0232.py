# Generated by Django 2.2.6 on 2019-12-05 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_auto_20191205_0205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='time_end',
        ),
        migrations.RemoveField(
            model_name='event',
            name='time_start',
        ),
        migrations.AlterField(
            model_name='event',
            name='date_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_start',
            field=models.DateTimeField(),
        ),
    ]
