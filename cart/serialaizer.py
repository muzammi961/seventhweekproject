from rest_framework import serializers
from .models import Cart,ItemCart,WishList,WishListUser
from adminuser.serializer import ProductSerializer;

class CartSerialaizer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields=['id','user']
class ItemCartSerialaizer(serializers.ModelSerializer):
    cart=CartSerialaizer()
    product=ProductSerializer()
    class Meta:
        model=ItemCart
        fields=['id','cart','product','quantity']        
        

class WishListUserSerialaizer(serializers.ModelSerializer):
    class Meta:
        model=WishListUser
        fields=['id','user']
class WishListSerialaizer(serializers.ModelSerializer):
    wishuser =WishListUserSerialaizer()
    product=ProductSerializer()
    class Meta:
        model=WishList
        fields=['id','wishuser','product']    
        
        
                  
        
        