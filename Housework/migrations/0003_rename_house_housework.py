# Generated by Django 4.2.7 on 2024-11-22 14:25

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Housework', '0002_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='House',
            new_name='Housework',
        ),
    ]
