# Generated by Django 2.2.6 on 2020-02-26 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0006_auto_20200225_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='phone',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
