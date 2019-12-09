# Generated by Django 2.2.6 on 2019-12-07 01:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_auto_20191206_2347'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DayOfWeek',
        ),
        migrations.AlterField(
            model_name='recurringevent',
            name='first_occurence',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.RecurringEvent'),
        ),
    ]