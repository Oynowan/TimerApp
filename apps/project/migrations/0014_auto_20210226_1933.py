# Generated by Django 3.1.6 on 2021-02-26 19:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_auto_20210226_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
