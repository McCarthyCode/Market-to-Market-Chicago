# Generated by Django 2.2.6 on 2019-12-26 22:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '__first__'),
        ('events', '0018_auto_20191218_0214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.Location'),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]
