# Generated by Django 3.1.6 on 2021-05-12 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('codes', '0001_initial'),
        ('team', '0006_auto_20210214_1952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitation',
            name='code',
        ),
        migrations.AddField(
            model_name='invitation',
            name='auth_key',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='codes.authenticationkey'),
            preserve_default=False,
        ),
    ]
