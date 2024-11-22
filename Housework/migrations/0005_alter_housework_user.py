# Generated by Django 4.2.7 on 2024-11-22 15:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Housework', '0004_alter_housework_houseworkdetail_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housework',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_housework', to=settings.AUTH_USER_MODEL),
        ),
    ]
