# Generated by Django 2.2.10 on 2021-02-05 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0027_auto_20210202_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='clienttask',
            name='is_approved_partner',
            field=models.BooleanField(default=False),
        ),
    ]
