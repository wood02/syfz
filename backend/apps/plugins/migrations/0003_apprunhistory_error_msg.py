# Generated by Django 3.1.13 on 2022-04-27 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plugins', '0002_auto_20220427_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='apprunhistory',
            name='error_msg',
            field=models.TextField(blank=True, null=True, verbose_name='错误信息'),
        ),
    ]