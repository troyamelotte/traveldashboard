from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime
EMAILCHECK = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def checkreg(self, name, user, password, confirm_password):
        errorlist = []
        count = 0
        if len(name)<2:
            errorlist.append('Name too short!')
            count +=1

        if len(user)<1:
            errorlist.append('Username is too short!')
            count+=1

        if not password==confirm_password:
            errorlist.append('Passwords are not the same!')
            count+=1
        elif len(password)<8:
            errorlist.append('Please enter a password longer than 8 characters!')
            count+=1

        if count==0:
            return True
        return errorlist

    def checklog(self, username, password):
        errorlist = []
        count = 0
        user = User.objects.get(username=username)
        password=password.encode()
        if not username == user.username:
            count+=1
            errorlist.append('Username incorrect')
        if bcrypt.hashpw(password, bcrypt.gensalt()) == user.password:
            count+=1
            errorlist.append('Password incorrect')

        if count == 0:
            return [True, user]
        return errorlist

class User(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    userManager = UserManager()
    objects = models.Manager()

class TripManager(models.Manager):
    def tripvalid(self, destination, description, datefrom, dateto):
        errorlist = []
        count = 0
        now = datetime.now()
        datefromstrip = datetime.strptime(datefrom, '%Y-%m-%d')
        datetostrip = datetime.strptime(dateto, '%Y-%m-%d')
        print datefromstrip
        if len(destination)<1:
            errorlist.append('Destination can not be empty!')
            count +=1

        if len(description)<1:
            errorlist.append('Description can not be empty!')
            count+=1

        if datefromstrip < now:
            errorlist.append('Please choose a future date!')
            count+=1

        if datefromstrip > datetostrip:
            errorlist.append('Date from must be before date to!')
            count+=1

        if count == 0:
            return True
        return errorlist



class Trip(models.Model):
    destination = models.CharField(max_length=50, default=None)
    description = models.TextField(max_length=1000)
    datefrom = models.DateField()
    dateto = models.DateField()
    created_by = models.ForeignKey('User', related_name='TripToCreator', default=None)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    tripManager = TripManager()
    objects = models.Manager()

class Attending(models.Model):
    trip_id = models.ForeignKey('Trip', related_name='AttendingToTrip')
    user_id = models.ForeignKey('User', related_name='AttendingToUser')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
