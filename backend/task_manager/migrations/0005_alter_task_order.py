# Generated by Django 4.2.19 on 2025-03-28 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0004_alter_task_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
