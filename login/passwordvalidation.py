# -*- coding: utf-8 -*-
"""
Created on Tue May 28 10:28:49 2019

@author: harid
"""
#import re for regular expressions
import re

class PasswordValidation:
#this function takes string and returns wheather it is valid or not        
    def validity(self, string):
        
        #if length of password is less than 8 than it is invalid
        if(len(string) < 8):
            return("Not valid")
        
        #checks for special character in string
        special = False
        
        if (re.search('[a-z]',string) and        #small letters
                re.search('[A-Z]',string) and    #capital letters
                    re.search('[0-9]',string)):  #numeric values
            
            for char in string:
                
                #condtion for special character
                if((ord(str(char))>=33 and 
                        ord(str(char))<=47) or 
                            (ord(str(char))>=58 and 
                                 ord(str(char))<=64)):
                    
                    #check the flag
                    special = True
            
            if(special == True):
                return("Valid")
            else:
                return("Not valid")
        
        else:
            return("Not valid")    