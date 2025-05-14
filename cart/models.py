from django.db import models
from authentication.models import CustomUser
from adminuser.models import ProductData
# Create your models here.

class Cart(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    
 
class ItemCart(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(ProductData,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
        