from rest_framework import serializers
from .models import Cart,ItemCart

class CartSerialaizer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields='__all__'

class ItemCartSerialaizer(serializers.ModelSerializer):
    cart=CartSerialaizer()
    class Meta:
        model=ItemCart
        fields='__all__'        
        
        