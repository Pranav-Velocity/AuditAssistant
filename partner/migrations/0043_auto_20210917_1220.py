# Generated by Django 2.2.10 on 2021-09-17 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0042_auto_20210917_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auditplanmapping',
            name='is_invoice_paid',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
