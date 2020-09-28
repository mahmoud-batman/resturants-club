# Generated by Django 3.1.1 on 2020-09-27 18:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurants', '0007_restaurantlocation_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantlocation',
            name='owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.customuser'),
        ),
    ]
