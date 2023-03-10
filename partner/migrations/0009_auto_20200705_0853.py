# Generated by Django 2.2.10 on 2020-07-05 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0008_activity_activity_lable'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity_Lables',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_lable_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='activity',
            name='activity_lable',
        ),
        migrations.AddField(
            model_name='activity',
            name='lable',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activity_lable', to='partner.Activity_Lables'),
        ),
    ]
