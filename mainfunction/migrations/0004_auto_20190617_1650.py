# Generated by Django 2.2.2 on 2019-06-17 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainfunction', '0003_dailydetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailydetails',
            name='task_status',
            field=models.CharField(max_length=5),
        ),
    ]