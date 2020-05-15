# Generated by Django 3.0.5 on 2020-05-14 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_auto_20200512_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Nightlife'), (1, 'Restaurants'), (3, 'Arts & Entertainment'), (4, 'Health & Fitness'), (5, 'Sports'), (6, 'Non-profit'), (7, 'Editorials & Opinions')], default=0),
        ),
    ]