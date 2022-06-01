# Generated by Django 3.1.13 on 2022-05-11 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alarm', '0030_auto_20220510_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='IcpZoomEyeToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('token', models.CharField(max_length=100, unique=True, verbose_name='Token')),
                ('status', models.PositiveSmallIntegerField(blank=True, choices=[(0, '未知'), (1, '正常'), (2, '异常')], default=0, null=True, verbose_name='状态')),
                ('rate_limit', models.JSONField(blank=True, default=dict, null=True, verbose_name='限制信息')),
                ('remark', models.CharField(blank=True, max_length=255, null=True, verbose_name='备注')),
                ('error_message', models.TextField(blank=True, null=True, verbose_name='异常信息')),
            ],
            options={
                'verbose_name': 'ZoomEye token',
                'verbose_name_plural': 'ZoomEye token',
                'db_table': 'passive_zoomeye_token',
                'ordering': ['-id'],
            },
        ),
    ]