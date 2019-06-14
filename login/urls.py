# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 12:04:19 2019

@author: harid
"""
from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
            path('', views.login, name='login'),
            path('signup/', views.signup, name='signup'),
            path('register/', views.register, name='register'),
            path('authenticate/', views.authenticate, name='authenticate')
        ]