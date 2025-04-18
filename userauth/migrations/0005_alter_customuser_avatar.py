# Generated by Django 5.1.6 on 2025-03-22 17:04

import userauth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0004_alter_customuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, default='profile_pics/default_avatar.jpg', null=True, upload_to=userauth.models.user_directory_path),
        ),
    ]
