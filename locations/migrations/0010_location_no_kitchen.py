# Generated by Django 2.2.6 on 2020-02-28 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0009_auto_20200227_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='no_kitchen',
            field=models.BooleanField(default=False),
        ),
    ]
