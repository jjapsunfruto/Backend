# Generated by Django 4.2.7 on 2024-11-24 10:42

import User.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='housecode',
            field=models.IntegerField(default=User.models.housecode, max_length=4, unique=True),
        ),
    ]
