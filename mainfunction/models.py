from django.db import models
from login.models import UserDetails
# Create your models here.
class ProjectDetails(models.Model):
    constructer_details = models.ForeignKey(UserDetails,
                                            on_delete=models.CASCADE)
    project_name = models.CharField(max_length=200)
    client_name = models.CharField(max_length=200)
    starting_date = models.DateField()
    ending_date = models.DateField()
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    
class DailyDetails(models.Model):
    project_details = models.ForeignKey(ProjectDetails, on_delete=models.CASCADE)
    day = models.IntegerField(primary_key=True)
    task_status = models.CharField(max_length=5)
    reason = models.CharField(max_length=200)