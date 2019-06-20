# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 17:36:57 2019

@author: harid
"""
from django.urls import path
from . import views

app_name = 'mainfunction'

urlpatterns = [
            path('', views.dashboard, name='dashboard'),
            path('additem/', views.add_item, name='add_item'),
            path('dailydetails/<project_name>/', views.add_daily_details,
                 name='add_daily_details')
        ]
