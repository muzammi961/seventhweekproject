from django.shortcuts import render
from adminuser.models import ProductData,Category_Product
from rest_framework.views import APIView
from rest_framework.views import Response
from .serialaizer import ViewProductsByCategorySerialaizer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from adminuser.serializer   import CategorySerializer
# Create your views here.

class ViewProductsByCategory(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,bycategory):
      try:  
       instance=Category_Product.objects.get(name=bycategory)
      except Category_Product.DoesNotExist:
          return Response(status=status.HTTP_404_NOT_FOUND)
      datas=ProductData.objects.filter(category_name=instance)
      serialaizer=ViewProductsByCategorySerialaizer(datas,many=True)
      return Response(serialaizer.data,status=status.HTTP_200_OK)

class ViewSpecificProduct(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,pk):
       try: 
        instance=ProductData.objects.get(pk=pk)
       except:
           return Response({'message':'data does not find.....'},status=status.HTTP_404_NOT_FOUND)
       serialaizer=ViewProductsByCategorySerialaizer(instance)
       return Response(serialaizer.data,status=status.HTTP_200_OK)
   

class Viewallproduct(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            values = ProductData.objects.all() # .filter() is optional here
            serializer = ViewProductsByCategorySerialaizer(values, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Data not retrieved', 'error': str(e)},status=status.HTTP_400_BAD_REQUEST)
        

class GetallCategory(APIView):
  permission_classes=[IsAuthenticated]
  def get(self,request):
    try:
      getcategory=Category_Product.objects.all()
      serializer=CategorySerializer(getcategory,many=True)
    except Category_Product.DoesNotExist:
      return Response({'message':'category does not existe.....'},status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data,status=status.HTTP_200_OK)            