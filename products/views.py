from django.shortcuts import render
from adminuser.models import ProductData,Category_Gender
from rest_framework.views import APIView
from rest_framework.views import Response
from .serialaizer import ViewProductsByCategorySerialaizer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class ViewProductsByCategory(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,bycategory):
      try:  
       instance=Category_Gender.objects.get(name=bycategory)
      except Category_Gender.DoesNotExist:
          return Response(status=status.HTTP_404_NOT_FOUND)
      datas=ProductData.objects.filter(category_name=instance)
      serialaizer=ViewProductsByCategorySerialaizer(datas,many=True) 
      return Response(serialaizer.data,status=status.HTTP_302_FOUND)

class ViewSpecificProduct(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,pk):
       try: 
        instance=ProductData.objects.get(pk=pk)
       except:
           return Response({'message':'data does not find.....'},status=status.HTTP_404_NOT_FOUND)
       serialaizer=ViewProductsByCategorySerialaizer(instance)
       return Response(serialaizer.data,status=status.HTTP_200_OK)