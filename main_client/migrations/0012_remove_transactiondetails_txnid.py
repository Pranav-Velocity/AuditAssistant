# Generated by Django 4.1.4 on 2023-01-18 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_client', '0011_temptransaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactiondetails',
            name='txnid',
        ),
    ]
