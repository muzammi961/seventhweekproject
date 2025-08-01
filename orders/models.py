from django.db import models
from cart.models import Cart
from adminuser.models import ProductData
from authentication.models import CustomUser

class Orderusre(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Orderitem(models.Model):
    user_forin = models.ForeignKey(Orderusre, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductData, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered_at = models.DateTimeField(auto_now_add=True)


class Useraddressuser(models.Model):
    username=models.OneToOneField(CustomUser,on_delete=models.CASCADE)                                                                                                                                                                     
class Useraddress(models.Model):
    nameofuser=models.CharField(max_length=100)
    phonenumber=models.BigIntegerField()
    pincode=models.IntegerField()
    state=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    houseno_buildingname=models.CharField(max_length=100)
    Roadname=models.CharField(max_length=100)
    adduser=models.OneToOneField(Useraddressuser,on_delete=models.CASCADE)