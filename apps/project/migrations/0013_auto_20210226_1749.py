# Generated by Django 3.1.6 on 2021-02-26 17:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0012_auto_20210226_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 26, 17, 49, 5, 385271)),
        ),
    ]
