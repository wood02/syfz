# Generated by Django 3.1.13 on 2022-03-30 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alarm', '0010_attack_fz_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailtaginfo',
            name='source',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, '未知'), (1, '微步'), (2, '绿盟')], default=1, null=True, verbose_name='来源'),
        ),
    ]
