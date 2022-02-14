# Generated by Django 3.1.6 on 2021-06-14 15:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('password_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='passwordstore',
            name='created_by',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.RESTRICT, to='auth.user', verbose_name='Created by user'),
            preserve_default=False,
        ),
    ]