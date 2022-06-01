# Generated by Django 3.1.13 on 2022-05-19 16:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Poc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('poc_id', models.CharField(blank=True, max_length=20, unique=True, verbose_name='PoC ID')),
                ('poc_name', models.CharField(max_length=50, verbose_name='PoC名称')),
                ('component', models.CharField(blank=True, max_length=20, verbose_name='影响组件')),
                ('version', models.CharField(blank=True, max_length=20, verbose_name='影响版本')),
                ('poc_desc', models.CharField(blank=True, max_length=50, verbose_name='PoC描述')),
                ('vulnerability', models.CharField(blank=True, max_length=50, verbose_name='关联漏洞')),
                ('method', models.CharField(max_length=20, verbose_name='请求方式')),
                ('path', models.CharField(max_length=100, verbose_name='路径')),
                ('header', models.TextField(blank=True, max_length=300, verbose_name='请求头')),
                ('cookie', models.CharField(blank=True, max_length=100, verbose_name='cookie')),
                ('params', models.JSONField(blank=True, max_length=200, verbose_name='参数')),
                ('status_code', models.CharField(blank=True, max_length=50, verbose_name='状态码')),
                ('content', models.CharField(blank=True, max_length=50, verbose_name='内容匹配字')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poc_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Poc',
                'verbose_name_plural': 'Poc',
                'db_table': 'syfz_poc',
                'ordering': ['-id'],
            },
        ),
    ]
