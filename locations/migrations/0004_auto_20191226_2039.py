# Generated by Django 2.2.6 on 2019-12-27 02:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_location_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='neighborhood',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.Neighborhood'),
        ),
        migrations.AlterField(
            model_name='location',
            name='slug',
            field=models.SlugField(blank=True, default='', editable=False, max_length=100, null=True),
        ),
    ]
