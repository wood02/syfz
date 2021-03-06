# Generated by Django 3.1.13 on 2022-04-18 10:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('system', '0003_auto_20220330_1552'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=255, null=True, verbose_name='用户名')),
                ('login_date', models.DateTimeField(blank=True, null=True, verbose_name='登录时间')),
                ('terminal_type', models.CharField(blank=True, max_length=50, null=True, verbose_name='终端类型')),
                ('browser_type', models.CharField(blank=True, max_length=50, null=True, verbose_name='浏览器类型')),
                ('os_type', models.CharField(blank=True, max_length=255, null=True, verbose_name='操作系统')),
                ('equipment_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='设备名称')),
                ('mac_address', models.CharField(blank=True, max_length=50, null=True, verbose_name='MAC地址')),
                ('login_ip', models.CharField(db_index=True, max_length=50, null=True, verbose_name='登录IP')),
                ('is_super', models.BooleanField(default=False, verbose_name='是否是超级用户')),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='login_event_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '登录记录',
                'verbose_name_plural': '登录记录',
                'db_table': 'syfz_sys_login_event',
                'ordering': ['-id'],
            },
        ),
    ]
