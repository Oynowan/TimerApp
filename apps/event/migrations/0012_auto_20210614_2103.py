# Generated by Django 3.1.6 on 2021-06-14 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0011_auto_20210614_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='child',
            field=models.BooleanField(default=False),
        ),
    ]