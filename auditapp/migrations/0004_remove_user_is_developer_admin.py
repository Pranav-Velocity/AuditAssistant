# Generated by Django 2.2.10 on 2020-05-29 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auditapp', '0003_auto_20200529_1546'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_developer_admin',
        ),
    ]
