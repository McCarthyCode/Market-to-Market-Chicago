# Generated by Django 2.2.6 on 2020-01-15 00:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0021_recurringevent_weekly'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recurringevent',
            name='first_occurence',
        ),
        migrations.RemoveField(
            model_name='recurringevent',
            name='weekly',
        ),
        migrations.CreateModel(
            name='RecurringEventInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('weekly', models.BooleanField(default=True)),
                ('first_occurence', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.RecurringEvent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='recurringevent',
            name='info',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='events.RecurringEventInfo'),
        ),
    ]