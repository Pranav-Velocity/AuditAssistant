# Generated by Django 2.2.10 on 2021-06-15 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0031_auditplanmapping_out_of_pocket_expenses'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditplanmapping',
            name='is_billable',
            field=models.BooleanField(default=False),
        ),
    ]
