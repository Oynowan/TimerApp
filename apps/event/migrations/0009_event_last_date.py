# Generated by Django 3.1.6 on 2021-06-12 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0008_event_parent_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='last_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
