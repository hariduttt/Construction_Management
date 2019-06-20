from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
import datetime
import json
from .forms import AddProjectDetails
from django.db import connection
from .models import ProjectDetails, DailyDetails
from login.models import UserDetails
from .weatherverification import WeatherValidation
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
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
        
    project_name_list = ProjectDetails.objects.filter(constructer_details
                                                      =user_details).values_list('project_name')
    project_location_list = ProjectDetails.objects.filter(constructer_details
                                                          =user_details).values_list('location')
    project_startdate_list = ProjectDetails.objects.filter(constructer_details
                                                           =user_details).values_list('starting_date')
    project_enddate_list = ProjectDetails.objects.filter(constructer_details
                                                           =user_details).values_list('ending_date')
    
    project_name = []
    project_location = []
    project_startdate = []
    project_enddate = []
    for i in range(len(project_name_list)):
        project_name.append(project_name_list[i][0])
        project_location.append(project_location_list[i][0])
        project_startdate.append(project_startdate_list[i][0])
        project_enddate.append(project_enddate_list[i][0])
    
    project_status = []
    project_days = []
    now = datetime.date.today()
    for date_start, date_end in zip(project_startdate, project_enddate):
        delta = now - date_start
        if(date_start > now):
            project_status.append("Upcoming")
        elif(date_start <= now and date_end >= now):
            project_status.append("Ongoing")
        elif(now > date_end):
            project_status.append("Completed")
        project_days.append(delta.days + 1)

    print(project_name)
    print(project_location)
    print(project_startdate)
    print(project_enddate)
    print(project_status)
    print(project_days)
        
    project_details_list = list(zip(project_name, project_location,
                                    project_days, project_status))
    print(project_details_list)
    context = {'user':user_name, 'project_details':project_details_list}
    
    return render(request, "mainfunction/dashboard.html", context)
        
def add_item(request):
    if(request.method == 'POST'):
        print("1")
        form = AddProjectDetails()
        print("2")
        form = AddProjectDetails(request.POST)
        if(form.is_valid()):
            try:
                form.clean_date()
            except ValidationError as error:
                print(repr(error.message))
                Response = HttpResponse(
                            json.dumps({'Error':repr(error.message)}),
                            content_type = "application/json"
                            )
                return Response
            Response = HttpResponse(
                            json.dumps({'Error':""}),
                            content_type = "application/json"
                            )
            return Response
        Response = HttpResponse(
                            json.dumps({'Error':"Some field(s) contains invalid data."}),
                            content_type = "application/json"
                            )
        return Response
    user_name = request.GET.get('user')
    form = AddProjectDetails()
    context = {'user':user_name, 'form':form}
    return render(request, "mainfunction/add_project_form.html", context)

def add_daily_details(request, project_name):
    user_name = request.GET.get("user")
    user_details = UserDetails.objects.get(user_name=user_name)
    project = ProjectDetails.objects.get(constructer_details=user_details,
                                         project_name=project_name)
    date = project.starting_date
    end_date = project.ending_date
    city = project.city
    now = datetime.date.today()
    delta = now - date
    message = ""
    if(now < date):
        message = "Project has not been started yet!"
    elif(end_date < now):
        message = "Project has been finished!"
    days = delta.days + 1
    invalid_reason = ""
    
    if(request.method == 'POST'):
        task_status = request.POST["inputTaskStatus"]
        reason = request.POST["inputReason"]
        if(task_status == "Not Completed"):
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

    context = {'user':user_name, 'days':days,'project_name':project_name,
               'daily_details':daily_details_list,
               'invalid_reason':invalid_reason,
               'message':message}

    return render(request, "mainfunction/add_daily_details.html", context)