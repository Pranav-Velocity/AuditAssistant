# Generated by Django 2.2.10 on 2020-06-15 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='industry',
            old_name='name',
            new_name='industry_name',
        ),
    ]