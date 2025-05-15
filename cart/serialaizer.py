from rest_framework import serializers
from .models import Cart,ItemCart,WishList,WishListUser

class CartSerialaizer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields='__all__'
class ItemCartSerialaizer(serializers.ModelSerializer):
    cart=CartSerialaizer()
    class Meta:
        model=ItemCart
        fields='__all__'        
        


class WishListUserSerialaizer(serializers.ModelSerializer):
    class Meta:
        model=WishListUser
        fields='__all__'
class WishListSerialaizer(serializers.ModelSerializer):
    wishuser =WishListUserSerialaizer()
    class Meta:
        model=WishList
        fields='__all__'        
        
        