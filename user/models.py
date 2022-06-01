from django.db import models
from django.core.validators import validate_email

# Create your models here.

class User(models.Model):
    first_Name = models.CharField(max_length=4 ,blank=False)
    Last_Name = models.CharField(max_length=254,blank=False)
    Email_id = models.EmailField(max_length=254,blank=False,)
    Mobile_Number = models.CharField(max_length=254,blank=False)
    Password = models.CharField(max_length=254,blank=False)