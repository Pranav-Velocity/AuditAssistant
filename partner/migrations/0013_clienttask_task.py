# Generated by Django 2.2.10 on 2020-09-01 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0012_auto_20200815_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='clienttask',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='partner.Task'),
        ),
    ]
