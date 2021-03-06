# Generated by Django 3.1.13 on 2021-11-24 10:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alarm', '0007_auto_20211124_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='xtbapikey',
            name='api_limit',
            field=models.IntegerField(default=50, verbose_name='API限制'),
        ),
        migrations.AddField(
            model_name='xtbapikey',
            name='api_remaining',
            field=models.IntegerField(default=50, validators=[django.core.validators.MinValueValidator(0)], verbose_name='API剩余'),
        ),
        migrations.AddField(
            model_name='xtbapikey',
            name='api_reset_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='重置时间'),
        ),
        migrations.AlterField(
            model_name='xtbapikey',
            name='status',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, '未知'), (1, '正常'), (2, '异常'), (3, '失效')], default=0, null=True, verbose_name='状态'),
        ),
    ]
