from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
import datetime
from django.db import connection
from .models import ProjectDetails, DailyDetails
from login.models import UserDetails
from .weatherverification import WeatherValidation
# Create your views here.
def dashboard(request):
    user_name = request.GET.get('user')
    user_details = UserDetails.objects.get(user_name=user_name)
    
    if(request.method == 'POST'):
        project_name = request.POST["inputProjectName"]
        client_name = request.POST["inputClientName"]
        starting_date = request.POST["inputStartingDate"]
        ending_date = request.POST["inputEndingDate"]
        location = request.POST["inputLocation"]
        city = request.POST["inputCity"]
        
        project_details_record = ProjectDetails(project_name = project_name,
                                                client_name = client_name,
                                                starting_date = starting_date,
                                                ending_date = ending_date,
                                                location = location,
                                                city = city,
                                                constructer_details 
                                                    = user_details)
        project_details_record.save()
        
    project_name_list = ProjectDetails.objects.filter(constructer_details=user_details).values_list('project_name')
    project_location_list = ProjectDetails.objects.filter(constructer_details=user_details).values_list('location')
    project_startdate_list = ProjectDetails.objects.filter(constructer_details=user_details).values_list('starting_date')

    project_name = []
    project_location = []
    project_startdate = []
    for i in range(len(project_name_list)):
        project_name.append(project_name_list[i][0])
        project_location.append(project_location_list[i][0])
        project_startdate.append(project_startdate_list[i][0])
    
    project_days = []
    now = datetime.date.today()
    for date in project_startdate:
        delta = now - date
        project_days.append(delta.days + 1)
    
    project_details_list = list(zip(project_name, project_location, project_days))
    context = {'user':user_name, 'project_details':project_details_list}
    
    return render(request, "mainfunction/dashboard.html", context)
        
def add_item(request):
    user_name = request.GET.get('user')
    context = {'user':user_name}
    
    return render(request, "mainfunction/add_project_form.html", context)

def add_daily_details(request, project_name):
    user_name = request.GET.get("user")
    user_details = UserDetails.objects.get(user_name=user_name)
    project = ProjectDetails.objects.get(constructer_details=user_details, project_name=project_name)
    date = project.starting_date
    city = project.city
    now = datetime.date.today()
    delta = now - date
    days = delta.days + 1
    invalid_reason = ""
    
    if(request.method == 'POST'):
        task_status = request.POST["inputTaskStatus"]
        reason = request.POST["inputReason"]
        if(task_status == "False"):
            weather_check = WeatherValidation()
            weather_info = weather_check.getWeather_from_City(city)
            print("weather_info")
            print(weather_info)
            check = weather_check.validate_reason(reason, weather_info)
            if(check):
                daily_details_record = DailyDetails(project_details=project,
                                                    day=days,
                                                    task_status=task_status,
                                                    reason=reason)
                daily_details_record.save()
            else:
                invalid_reason = "Reason of bad weather is invalid!"
                daily_details_record = DailyDetails(project_details=project,
                                                    day=days,
                                                    task_status=task_status,
                                                    reason="No valid reason.")
                daily_details_record.save()
        else:
            daily_details_record = DailyDetails(project_details=project,
                                                day=days,
                                                task_status=task_status,
                                                reason="All Good")
            daily_details_record.save()
        
    daily_days_list = DailyDetails.objects.filter(project_details=project).values_list('day')
    daily_taskstatus_list = DailyDetails.objects.filter(project_details=project).values_list('task_status')
    daily_reason_list = DailyDetails.objects.filter(project_details=project).values_list('reason')
    
    daily_days = []
    daily_taskstatus = []
    daily_reason = []
    
    for i in range(len(daily_days_list)):
        daily_days.append(daily_days_list[i][0])
        daily_taskstatus.append(daily_taskstatus_list[i][0])
        daily_reason.append(daily_reason_list[i][0])
    
    daily_details_list = list(zip(daily_days, daily_taskstatus, daily_reason))
    print(daily_details_list)
    
    context = {'user':user_name, 'days':days,'project_name':project_name,
               'daily_details':daily_details_list,
               'invalid_reason':invalid_reason}
    
    return render(request, "mainfunction/add_daily_details.html", context)