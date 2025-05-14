from django.shortcuts import render
from rest_framework.response import Response
from django.shortcuts import  get_object_or_404
from adminuser.models import ProductData

from rest_framework.views import APIView
from .models import Cart,ItemCart
from rest_framework import status
# Create your views here.
class AddProductCart(APIView):
    def post(self,request):
        user=request.user
        product_id=request.data.get('product')
        quantity=request.data.get('quantity')
        print('it is the quantity ::',quantity,'it is the product id ::',product_id)
        if not product_id or not quantity:
          return Response({'message':'product and quantity not get'},status=status.HTTP_400_BAD_REQUEST)
        try:
          product=ProductData.objects.get(id=product_id)
        except:
          return Response({'message':'product id not get'},status=status.HTTP_404_NOT_FOUND)  
        
        item,_=Cart.objects.get_or_create(user=user)
        get_,created=ItemCart.objects.get_or_create(cart=item,product=product)
        if created:
          get_.quantity=int(quantity)
        else:
          get_.quantity+=int(quantity)
        get_.save()
        return Response({'message':'product cart add successfully ...'},status=status.HTTP_201_CREATED)    
        