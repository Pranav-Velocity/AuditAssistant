# Generated by Django 4.1.4 on 2023-01-05 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0047_clienttask_task_end_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clienttask',
            name='article_attachment_file',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clienttask',
            name='auditor_attachment_file',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clienttask',
            name='manager_attachment_file',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clienttask',
            name='partner_attachment_file',
            field=models.TextField(blank=True, null=True),
        ),
    ]