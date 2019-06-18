# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 10:54:38 2019

@author: harid
"""
import json
import urllib.request

class WeatherValidation:
    
    def getCoordinates_from_Location(self, location):
        geolocation_api_key = "75a6dd4caab84fd887f712babb30ece6"
        geolocation_request_url = "https://api.opencagedata.com/geocode/v1/"\
                                    "json?q=" + location + "&key="\
                                    + geolocation_api_key
         
        with urllib.request.urlopen(geolocation_request_url) as url:
            data = json.loads(url.read().decode())
        
        coordinates = data["results"][0]["annotations"]["DMS"]
        
        return coordinates
    
    '''def getWeather_from_Coordinates(self, latitude, longitude):
        weather_api_key = "d45710ade943b6f624924d8191198356&units=Metric"
        weather_request_url = "api.openweathermap.org/data/2.5/weather?"\
                                "lat=" + latitute + "&lon=" + lonngitude + "&appid=" + weather_api_key
                                
        
        with urllib.request.urlopen(geolocation_request_url) as url:
            data = json.loads(url.read().decode())
            
        return 0'''
            
    def getWeather_from_City(self, city):
        weather_api_key = "d45710ade943b6f624924d8191198356"
        weather_request_url = "https://api.openweathermap.org/data/2.5/weather?"\
                                "q=" + city + "&appid=" + weather_api_key
        
        with urllib.request.urlopen(weather_request_url) as url:
            data = json.loads(url.read().decode())
        
        weather_information = data["weather"][0]["main"]
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        wind_speed = data["wind"]["speed"]
        
        weather_dictionary = {"weather_information":weather_information,
                              "weather_description":weather_description,
                              "temperature":temperature,
                              "wind_speed":wind_speed}
    
        return weather_dictionary 
    
    def validate_reason(self, reason, weather_dictionary):
        if(reason == "Heavy Rain" 
           and (weather_dictionary["weather_information"] == "Heavy Rain"
                or weather_dictionary["weather_information"] == "Rain"
                or weather_dictionary["weather_description"] == "Extreme")):
            return True
        elif(reason == "Storm"
            and (weather_dictionary["weather_information"] == "Storm"
                 or weather_dictionary["weather_description"] == "Extreme")):
           return True
        elif(reason == "High Wind/Cyclone" 
             and (weather_dictionary["weather_information"] == "Cyclone"
                  or weather_dictionary["weather_information"] == "Wind"
                  or weather_dictionary["weather_description"] == "Extreme"
                  or int(weather_dictionary["wind_speed"]) >= 20)):
           return True
        elif(reason == "Snowfall" 
             and (weather_dictionary["weather_information"] == "Snowfall"
                  or weather_dictionary["weather_information"] == "Snow"
                  or weather_dictionary["weather_description"] == "Extreme"
                  or weather_dictionary["weather_description"] == "Snow"
                  or int(weather_dictionary["temperature"]) <= 283)):
           return True
        elif(reason == "Heat wave/Strong sun" 
             and int(weather_dictionary["temperature"]) >= 313):
           return True
        elif(reason == "All Good"):
           return True
        else:
           return False