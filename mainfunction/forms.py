# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 17:54:59 2019

@author: harid
"""
import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class AddProjectDetails(forms.Form):
    inputProjectName = forms.CharField(
                    label = "Project Name",
                    required=True,
                    widget = forms.TextInput(attrs={'class':'form-control',
                                                    'id':"inputProjectName",
                                                    'name':"inputProjectName",
                                                    'placeholder':"Name of the project"}),
                    max_length=200
                    )
    inputClientName = forms.CharField(
                    label = "Client Name",
                    required=True,
                    widget = forms.TextInput(attrs={'class':'form-control',
                                                    'id':"inputClientName",
                                                    'name':"inputClientName",
                                                    'placeholder':"Name of the client"}),
                    max_length=200
                    )
    inputStartingDate = forms.DateField(
                    label = "Starting Date",
                    required=True,
                    widget = forms.DateInput(attrs={'class':'form-control',
                                                    'type':'Date',
                                                    'id':'inputStartingDate',
                                                    'name':'inputStartingDate',
                                                    'onchange':"date_check('inputStartingDate')"})
                    )
    inputEndingDate = forms.DateField(
                    label = "Ending Date",
                    required=True,
                    widget = forms.DateInput(attrs={'class':'form-control',
                                                    'type':'Date',
                                                    'id':'inputEndingDate',
                                                    'name':'inputEndingDate',
                                                    'onchange':"date_cmp('inputEndingDate')"})
                    )
    inputLocation = forms.CharField(
                    label = "Location",
                    required=True,
                    widget = forms.TextInput(attrs={'class':'form-control',
                                                    'id':'inputLocation',
                                                    'name':'inputLocation',
                                                    'placeholder':"Entre the location of the construction"}),
                    max_length=200
                    )
    inputCity = forms.CharField(
                    label = "City",
                    required=True,
                    widget = forms.TextInput(attrs={'class':'form-control',
                                                    'id':'inputCity',
                                                    'name':'inputCity',
                                                    'placeholder':"City"}),
                    max_length=200
                    )
    
    def clean_date(self):
        date_starting = self.cleaned_data['inputStartingDate']
        date_ending = self.cleaned_data['inputEndingDate']
        
        # Check if a date is not in the past. 
        if(date_starting < datetime.date.today() or date_ending < datetime.date.today()):
            raise ValidationError(_('Starting/Ending date must not be in past.'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if(date_starting > date_ending):
            raise ValidationError(_('Starting date must be less than ending date.'))

        # Remember to always return the cleaned data.
        return date_starting, date_ending
    