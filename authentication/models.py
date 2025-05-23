from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
import random
# Create your models here.
class CustomUser(AbstractUser):
    username=models.CharField(max_length=100,unique=True)
    email=models.EmailField(max_length=100,unique=True)
    

   
    otp=models.IntegerField(null=True,blank=True)
    otp_expiration=models.DateTimeField(blank=True,null=True) 
    otp_varified=models. BooleanField(default=False)
    
    
    USERNAME_FIELD='username'
    REQUIRED_FIELDS=['email']
    
    def otp_generate(self):
        self.otp = random.randint(100000, 999999)
        self.otp_expiration=timezone.now()+timedelta(minutes=5)
        self.otp_varified=False
        self.save()
