# Generated by Django 4.1.4 on 2023-01-18 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auditapp', '0009_user_is_super_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mobile',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
