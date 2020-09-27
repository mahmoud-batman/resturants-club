# Generated by Django 3.1.1 on 2020-09-27 09:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='date_joined',
        ),
        migrations.AddField(
            model_name='customuser',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
