# Generated by Django 2.2.10 on 2020-07-05 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0010_auto_20200705_0944'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Activity_Lables',
            new_name='Activity_Labels',
        ),
        migrations.RenameField(
            model_name='activity',
            old_name='lable',
            new_name='label',
        ),
        migrations.RenameField(
            model_name='activity_labels',
            old_name='activity_lable_name',
            new_name='activity_label_name',
        ),
    ]