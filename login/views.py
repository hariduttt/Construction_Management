from django.shortcuts import render
import sys
from .models import UserDetails
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from login.passwordvalidation import PasswordValidation
from django.db import connection
# Create your views here.

def signup(request):
    error = request.GET.get('error')
    
    if(error == 'email_exists'):
        context = {'error':"Email ID already exists!"}
        return render(request, "login/signup_form.html", context)
    
    elif(error == 'invalid_password'):
        context = {'error':"Invalid Password!\nPassword should contain"\
                   " atleast one small letter, capital letter, number and a"\
                   " special character.The length should be atleast "\
                   "8 characters."}
        return render(request, "login/signup_form.html", context)
    
    else:
        return render(request, "login/signup_form.html")

def login(request):
    error = request.GET.get('error')
    if(error == 'wrong'):
        context = {'error':"Wrong Username or Password!"}
        
        return render(request, "login/login_form.html", context)
    else:
        
        return render(request, "login/login_form.html")
    
def register(request):
    user_name = request.POST['inputUname']
    u_email = request.POST['inputEmail']
    u_password = request.POST['inputPassword']
    try:
        u_name = UserDetails.objects.get(email=u_email)
    except:
        Validate_Password = PasswordValidation()
        validity_check = Validate_Password.validity(u_password)
        
        if(validity_check == "Valid"):
            ud_object = UserDetails(user_name=user_name, email=u_email,
                            password=u_password)
            ud_object.save()
        
            return HttpResponseRedirect(reverse("login:login"))
        else:
            return HttpResponseRedirect(reverse("login:signup")
                                        + "?error=invalid_password")
            
    return HttpResponseRedirect(reverse("login:signup")
                                + "?error=email_exists")
    
def authenticate(request):
    u_email = request.POST['inputEmail']
    u_password = request.POST['inputPassword']

    cursor = connection.cursor()
    
    cursor.execute("SELECT user_name FROM `login_userdetails`"\
                                         "WHERE email='" + u_email
                                         + "' and BINARY password='"
                                         +u_password + "'")
    u_name_tupple = cursor.fetchone()
    
    if(u_name_tupple == None):
        return HttpResponseRedirect(reverse("login:login") + "?error=wrong")
    
    u_name = u_name_tupple[0]
    if(u_name != "" or u_name != None):
        return HttpResponseRedirect(reverse("mainfunction:dashboard") 
                                    + "?user=" + str(u_name))