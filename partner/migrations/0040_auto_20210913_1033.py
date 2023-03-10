# Generated by Django 2.2.10 on 2021-09-13 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0039_auto_20210622_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditplanmapping',
            name='invoice_amount_paid',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='auditplanmapping',
            name='invoice_paid_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='auditplanmapping',
            name='is_invoice_paid',
            field=models.BooleanField(default=False),
        ),
    ]
