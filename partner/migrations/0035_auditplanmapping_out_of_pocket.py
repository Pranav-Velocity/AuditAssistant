# Generated by Django 2.2.10 on 2021-06-22 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0034_auto_20210620_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditplanmapping',
            name='out_of_pocket',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
