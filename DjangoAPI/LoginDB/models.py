from django.db import models

"""
Create models to store data
"""

"""
Model for storing user data
"""
# Create your models here.
class Users(models.Model):
    first = models.CharField(max_length=100)
    last = models.CharField(max_length=100)
    pw = models.CharField(max_length=100)
    email = models.CharField(max_length=100)    #Will be email, taken care at frontend
    name = models.CharField(max_length=100)
    
    # class Meta:
    #     unique_together = (("email", "name"),)

"""
Model for storing the files uploaded by the user, can be used to implement previous results.
"""
class Files(models.Model):
    username = models.CharField(max_length=100)
    files = models.FileField()
