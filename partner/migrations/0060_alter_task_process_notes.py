# Generated by Django 4.1.4 on 2023-02-22 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0059_alter_activity_process_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='process_notes',
            field=models.FileField(blank=True, max_length=500, null=True, upload_to='process_notes/'),
        ),
    ]
