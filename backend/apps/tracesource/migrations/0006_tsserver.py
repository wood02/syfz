# Generated by Django 3.1.13 on 2022-04-29 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracesource', '0005_auto_20220421_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='TsServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('server_type', models.CharField(max_length=50, verbose_name='服务类型')),
                ('ip', models.GenericIPAddressField(db_index=True, protocol='ipv4', verbose_name='IP')),
                ('port', models.IntegerField(blank=True, null=True, verbose_name='端口')),
                ('secret_key', models.TextField(blank=True, null=True, verbose_name='密钥')),
                ('status', models.CharField(blank=True, max_length=50, null=True, verbose_name='状态')),
            ],
            options={
                'verbose_name': '溯源服务器',
                'verbose_name_plural': '溯源服务器',
                'db_table': 'syfz_ts_server',
                'ordering': ['-id'],
            },
        ),
    ]
