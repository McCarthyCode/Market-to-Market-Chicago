# Generated by Django 2.2.6 on 2019-12-26 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('category', models.PositiveSmallIntegerField(choices=[(0, 'Nightlife'), (1, 'Restaurants'), (2, 'Arts & Entertainment'), (3, 'Health & Fitness'), (4, 'Sports'), (5, 'Non-profit')])),
                ('address1', models.CharField(max_length=200)),
                ('address2', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(default='Chicago', max_length=80)),
                ('state', models.CharField(default='IL', max_length=2)),
                ('zip_code', models.CharField(blank=True, max_length=5, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]