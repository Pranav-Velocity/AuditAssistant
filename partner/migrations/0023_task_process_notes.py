# Generated by Django 2.2.10 on 2021-01-07 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0022_auto_20210106_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='process_notes',
            field=models.FileField(blank=True, null=True, upload_to='process_notes/'),
        ),
    ]
