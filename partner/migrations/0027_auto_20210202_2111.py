# Generated by Django 2.2.10 on 2021-02-02 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0026_client_partner_incharge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='partner_incharge',
            new_name='assigned_partner',
        ),
    ]