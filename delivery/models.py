from django.db import models

# Create your models here.
class customers(models.Model):
    username = models.CharField( max_length=10)
    password = models.CharField( max_length=15)
    email = models.CharField( max_length=20)
    mobile = models.CharField( max_length=10)
    address = models.CharField( max_length=50)

def __str__(self):
    return self.username
