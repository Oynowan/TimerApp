# Generated by Django 3.1.6 on 2021-04-23 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_userprofile_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_hr',
            field=models.BooleanField(default=False),
        ),
    ]