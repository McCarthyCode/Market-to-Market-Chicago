# Generated by Django 2.2.6 on 2020-03-10 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20200310_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='_thumbnail_hash',
            field=models.BinaryField(blank=True, default=None, max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='thumbnail',
            field=models.ImageField(default=None, editable=False, null=True, upload_to='people/'),
        ),
    ]
