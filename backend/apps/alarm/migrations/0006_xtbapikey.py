# Generated by Django 3.1.13 on 2021-11-24 09:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alarm', '0005_fofatoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='XtbApiKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(blank=True, max_length=255, null=True, verbose_name='用户名')),
                ('apikey', models.CharField(max_length=64, unique=True, verbose_name='ApiKey')),
                ('status', models.PositiveSmallIntegerField(blank=True, choices=[(0, '未知'), (1, '正常'), (2, '异常')], default=0, null=True, verbose_name='状态')),
                ('error_msg', models.CharField(blank=True, max_length=255, null=True, verbose_name='错误信息')),
                ('error_num', models.IntegerField(default=0, help_text='错误次数', validators=[django.core.validators.MinValueValidator(0)], verbose_name='异常次数')),
                ('status_change_at', models.DateTimeField(blank=True, null=True, verbose_name='状态改变时间')),
                ('remark', models.CharField(blank=True, max_length=255, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': 'XtbApiKey',
                'verbose_name_plural': 'XtbApiKey',
                'db_table': 'passive_xbt_apikey',
                'ordering': ['-id'],
            },
        ),
    ]