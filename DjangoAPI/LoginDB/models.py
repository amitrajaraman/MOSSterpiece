from django.db import models

# Create your models here.
class Users(models.Model):
    first = models.CharField(max_length=100)
    last = models.CharField(max_length=100)
    pw = models.CharField(max_length=100)
    email = models.CharField(max_length=100)    #Will be email, taken care at frontend
    name = models.CharField(max_length=100)
    
    class Meta:
        unique_together = (("email", "name"),)

class Files(models.Model):
    username = models.CharField(max_length=100)
    files = models.FileField()
