# Generated by Django 3.1.13 on 2022-05-25 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracesource', '0007_auto_20220524_1335'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tsserver',
            old_name='cup_rate',
            new_name='cpu_rate',
        ),
    ]
