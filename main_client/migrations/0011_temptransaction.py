# Generated by Django 4.1.4 on 2023-01-18 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_client', '0010_billingtransaction_transactiondetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_client', models.CharField(max_length=100)),
                ('transactionID', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'temptransaction',
            },
        ),
    ]
