# Generated by Django 2.2.10 on 2020-07-05 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0007_regulator_type_of_audits'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='activity_lable',
            field=models.CharField(default='', max_length=255),
        ),
    ]
