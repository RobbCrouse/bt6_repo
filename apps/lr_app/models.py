from __future__ import unicode_literals

from django.db import models
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

import bcrypt

# Create your models here.

class UserManager(models.Manager):

    def register_validation(self, postData):

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        errors = []
        if len(postData['name']) < 3:
            errors.append("Your name is too short")
        if len(postData['username']) < 3:
            errors.append("Your Alias is too short")
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("You must submit a valid email")
        if len(postData['password']) < 8:
            errors.append("Your password is too short")        
        if postData['password'] != postData['c_password']:
            errors.append("Your passwords do not match")
        # try:
        #     if datetime.strptime(postData["hireday"], '%Y-%m-%d') > datetime.now():
        #         errors.append("You must be hired.")
        # except ValueError: 
        #     errors.append("Please enter a valid date")

        if len(errors) > 0:
            return (False, errors)
        else:

            hash_pw = bcrypt.hashpw(postData['password'].encode('utf-8'), bcrypt.gensalt())

            u = User.objects.create(name=postData['name'], username=postData['username'], password=hash_pw, email=postData['email'])
            return (True, u)


    def login_validation(self, postData):

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        errors = []
        # if len(postData['username']) < 3:
        #     errors.append("You must submit a valid Username")
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("You must submit a valid email")
        if len(postData['password']) < 8:
            errors.append("Your password is too short")

        if len(errors) > 0:
            return (False, errors)
        else:
            u = User.objects.filter(email=postData['email'])
            # QuerySet[<User Obj>]
            if u: # check to see if i got a user based on username
                print "found a user", 0
                if bcrypt.checkpw(postData['password'].encode('utf-8'), u[0].password.encode('utf-8')):
                
                    # if true, username and password matches what is in DB
                    return (True, u[0]) # <User Obj>
                    
                else:
                    errors.append("Password is incorrect") 
                    return(False, errors)
            else:
                print "did not find user"
                errors.append("No user exists with this Email.") 
                return(False, errors)

class User(models.Model):
    name = models.CharField(max_length=25)
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=50)
    # hireday = models.DateField()
    email = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
	    return 'name: {}, username: {}'.format(self.name, self.username)