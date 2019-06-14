from django.shortcuts import render
import sys
from .models import UserDetails
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

def signup(request):
    return render(request, "login/signup_form.html")

def login(request):
    error = request.GET.get('error')
    if(error == 'wrong'):
        context = {error:"Wrong Username or Password!"}
        return render(request, "login/login_form.html", context)
    else:
        return render(request, "login/login_form.html")
    
def register(request):
    user_name = request.POST['inputUname']
    u_email = request.POST['inputEmail']
    u_password = request.POST['inputPassword']

    ud_object = UserDetails(user_name=user_name, email=u_email,
                            password=u_password)
    ud_object.save()
    return HttpResponseRedirect(reverse("login:login"))
    
def authenticate(request):
    u_email = request.POST['inputEmail']
    u_password = request.POST['inputPassword']
    
    try:
        u_name = UserDetails.objects.get(email=u_email, password=u_password)
    except:
        return HttpResponseRedirect(reverse("login:login") + "?error=wrong")
    
    if(u_name.user_name != ""):
        return HttpResponse("Welcome " + u_name.user_name)