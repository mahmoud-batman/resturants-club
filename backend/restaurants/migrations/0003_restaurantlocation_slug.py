# Generated by Django 3.1.1 on 2020-09-25 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0002_auto_20200925_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurantlocation',
            name='slug',
            field=models.SlugField(default=1),
            preserve_default=False,
        ),
    ]
