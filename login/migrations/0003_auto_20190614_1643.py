# Generated by Django 2.2.2 on 2019-06-14 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20190614_1635'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetails',
            name='id',
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='email',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]
