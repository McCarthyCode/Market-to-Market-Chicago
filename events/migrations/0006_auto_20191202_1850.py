# Generated by Django 2.2.6 on 2019-12-02 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20191202_1831'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='event',
            managers=[
            ],
        ),
        migrations.RenameField(
            model_name='event',
            old_name='title',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='location',
            old_name='zip',
            new_name='zip_code',
        ),
    ]
