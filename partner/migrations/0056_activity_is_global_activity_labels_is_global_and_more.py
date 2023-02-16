# Generated by Django 4.1.4 on 2023-02-14 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0055_alter_regulator_type_of_audits'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='is_global',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='activity_labels',
            name='is_global',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='audits',
            name='is_global',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='audittype',
            name='is_global',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='entity',
            name='is_global',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='industry',
            name='is_global',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='regulator',
            name='is_global',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='task',
            name='is_global',
            field=models.BooleanField(default=False),
        ),
    ]