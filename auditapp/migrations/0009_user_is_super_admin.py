# Generated by Django 2.2.10 on 2022-12-28 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auditapp', '0008_auto_20221018_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_super_admin',
            field=models.BooleanField(default=False),
        ),
    ]
