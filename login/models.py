from django.db import models

# Create your models here.
class UserDetails(models.Model):
    user_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, primary_key=True)
    password = models.CharField(max_length=200)
