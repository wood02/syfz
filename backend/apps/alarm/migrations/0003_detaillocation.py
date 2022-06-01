# Generated by Django 3.1.13 on 2021-11-16 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alarm', '0002_detaildomain_detailtaginfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('location', models.JSONField(blank=True, default=list, null=True, verbose_name='地理位置信息')),
                ('attack', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detail_location', to='alarm.attack', verbose_name='攻击日志')),
            ],
            options={
                'verbose_name': '攻击详情-地理位置信息',
                'verbose_name_plural': '攻击详情-地理位置信息',
                'db_table': 'alarm_detail_location',
                'ordering': ['-id'],
            },
        ),
    ]
