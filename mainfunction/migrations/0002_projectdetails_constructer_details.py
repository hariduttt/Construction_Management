# Generated by Django 2.2.2 on 2019-06-17 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_auto_20190614_1643'),
        ('mainfunction', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectdetails',
            name='constructer_details',
            field=models.ForeignKey(default='Null', on_delete=django.db.models.deletion.CASCADE, to='login.UserDetails'),
            preserve_default=False,
        ),
    ]
