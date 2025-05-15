from django.shortcuts import render
from rest_framework.views import APIView 
from .serializer import AdminViewallUserSerializer,ProductSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from authentication.models import CustomUser
from rest_framework.response import Response
from .models import ProductData
from rest_framework import status
# Create your views here.

class AdminViewallUser(APIView):
  def get(self,request):
      user_data=CustomUser.objects.all()
      serializer=AdminViewallUserSerializer(user_data,many=True)
      print(serializer.data)
      return Response(serializer.data,status=status.HTTP_200_OK)
  
class ViewSpecificUserDetails(APIView):
    def get(self,request,pk):
        try:
          user_data=CustomUser.objects.get(pk=pk)
          serializer=AdminViewallUserSerializer(user_data)
        except:
          return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data,status=status.HTTP_302_FOUND) 
    

class CreateProductView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      

      
class GetallProducts(APIView):
  def get(self,request):
        data=ProductData.objects.all()
        serializer=ProductSerializer(data,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
      
      

class ViewAllProductbyCategory(APIView):
    def get(self, request, valuebycategory):
        products = ProductData.objects.filter(category__name=valuebycategory)
        if products.exists():
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'No products found for this category.'}, status=status.HTTP_404_NOT_FOUND)
          
          
class DeleteaProduct(APIView):
  def delete(self,request,pk):
    try:
      data=ProductData.objects.get(pk=pk)
      data.delete()
    except:
      return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Product deleted successfully','data':ProductSerializer(data).data},status=status.HTTP_200_OK)
              
              
class UpdateProductView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    def put(self, request, pk):
        try:
            product = ProductData.objects.get(pk=pk)
        except ProductData.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            updated = serializer.save()
            return Response(ProductSerializer(updated).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
