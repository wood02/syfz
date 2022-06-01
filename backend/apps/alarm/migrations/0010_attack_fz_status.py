# Generated by Django 3.1.13 on 2022-03-30 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alarm', '0009_hacker_vulnerability'),
    ]

    operations = [
        migrations.AddField(
            model_name='attack',
            name='fz_status',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, '待反制'), (1, '正在反制'), (2, '已完成')], default=0, null=True, verbose_name='反制状态'),
        ),
    ]
