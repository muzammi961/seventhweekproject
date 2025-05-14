from django.db import models

# Create your models here.
class Category_Gender(models.Model):
    name=models.CharField(max_length=100)
class ProductData(models.Model):
    productname=models.CharField(max_length=100,null=True)
    price = models.IntegerField()
    offer_price = models.IntegerField(default=0)
    size=models.IntegerField()
    item_photo = models.ImageField(upload_to='menu_photo/', blank=True, null=True)
    category=models.ForeignKey(Category_Gender,on_delete=models.CASCADE)