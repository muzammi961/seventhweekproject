from django.db import models

# Create your models here.
class Category_Product(models.Model):
    name=models.CharField(max_length=100)
class ProductData(models.Model):
    productname=models.CharField(max_length=100,null=True)
    price = models.IntegerField()
    offer_price = models.IntegerField(default=0)
    item_photo = models.ImageField(upload_to='menu_photo/', blank=True, null=True)
    category_name=models.ForeignKey(Category_Product,on_delete=models.CASCADE)