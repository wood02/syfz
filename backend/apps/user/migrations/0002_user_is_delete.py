# Generated by Django 3.1.13 on 2022-04-14 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
    ]