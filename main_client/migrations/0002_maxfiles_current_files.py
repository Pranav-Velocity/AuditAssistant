# Generated by Django 2.2.10 on 2022-11-02 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_client', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='maxfiles',
            name='current_files',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
