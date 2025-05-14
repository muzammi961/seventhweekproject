from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    username=models.CharField(max_length=100,unique=True)
    email=models.EmailField(max_length=100,unique=True)
    
    
    USERNAME_FIELD='username'
    REQUIRED_FIELDS=['email']