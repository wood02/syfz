# Generated by Django 3.1.13 on 2022-05-09 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alarm', '0028_attack_fz_task_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='attack',
            name='fz_result_raw',
            field=models.JSONField(blank=True, default=dict, null=True, verbose_name='反制结果'),
        ),
    ]
