from django.shortcuts import render
import sys
import random
from .models import UserDetails
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from login.passwordvalidation import PasswordValidation
from django.db import connection
from django.core.mail import BadHeaderError, send_mail
# Create your views here.
counter = 0

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
            try:
                code = random.randint(1,1000000)
                print(code)
                subject = "Registration Code"
                message = "Your registration code is : " + str(code) +"\n\n\nWith"\
                " Regard,\nHaridutt Jani"
                from_email = "hariduttjani@gmail.com"
                to_mail = u_email
                send_mail(subject, message, from_email,
                          [to_mail])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            context = {'error':'', 'code':code, 'email':u_email, 'counter':0}
            return render(request, 'login/confirmation.html', context)
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
def confirmation(request):
    email = request.GET.get('email')
    code = request.POST["code"]
    confirmation_code = request.POST["inputCode"]
    
    print(int(code))
    print(int(confirmation_code))
    if(int(confirmation_code) == int(code)):
        return HttpResponseRedirect(reverse("login:login")
                                    + "?Registration Successfully!")
    else:
        count = request.POST["counter"]
        
        if(int(count) >= 3):
            UserDetails.objects.filter(email=email).delete()
            return HttpResponseRedirect(reverse("login:signup"))
        else:
            counter = int(count) + 1
            if(int(count) == 2):
                error = "This is your last chance, else you will be redirected to signup page again."
            else:
                error = 'Incorrect Code!'
            context = {'error':error, 'code':code,
                       'email':email, 'counter':counter}
            return render(request, 'login/confirmation.html', context)