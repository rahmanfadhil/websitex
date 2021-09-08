# Generated by Django 3.2.6 on 2021-09-08 01:36

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='user_avatar/', verbose_name='profile picture'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits, underscores, and hyphens only.', max_length=150, null=True, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator(message='Enter a valid username. This value may contain only letters, numbers, underscores, and hyphens.', regex='^[\\w-]+\\Z')], verbose_name='username'),
        ),
    ]