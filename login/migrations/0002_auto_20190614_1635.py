# Generated by Django 2.2.2 on 2019-06-14 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='email',
            field=models.CharField(max_length=200, verbose_name='primary_key'),
        ),
    ]
