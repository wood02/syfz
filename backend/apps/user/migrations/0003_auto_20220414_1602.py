# Generated by Django 3.1.13 on 2022-04-14 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_is_delete'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_delete',
            new_name='is_deleted',
        ),
    ]