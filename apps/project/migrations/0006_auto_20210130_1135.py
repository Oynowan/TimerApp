# Generated by Django 3.1.5 on 2021-01-30 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_auto_20210130_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
