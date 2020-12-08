from django.db import models

## User model, for storing the user's data in database
class Users(models.Model):
    """
    Model for storing user data
    """
    first = models.CharField(max_length=100)
    last = models.CharField(max_length=100)
    pw = models.CharField(max_length=100)
    email = models.CharField(max_length=100)    #Will be email, taken care at frontend
    name = models.CharField(max_length=100)
    
    # class Meta:
    #     unique_together = (("email", "name"),)

## Model for storing data regarding files; originally implemented for creating a previous results page.
class Files(models.Model):
    """
    Model for storing the files uploaded by the user, can be used to implement previous results.
    """
    username = models.CharField(max_length=100)
    files = models.FileField()
