# Generated by Django 3.1.5 on 2021-01-28 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0002_auto_20210128_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='team',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
