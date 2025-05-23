from django.shortcuts import render
from rest_framework.views import APIView 
from .serializer import AdminViewallUserSerializer,ProductSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from authentication.models import CustomUser
from rest_framework.response import Response
from .models import ProductData,Category_Gender
from rest_framework import status
from django.http import Http404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from orders.serialaizer  import OrderDetileserializer
from orders.models import Orderitem,Orderusre      
from adminuser.serializer import ProductSerializer  
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
            from_user_data=serializer.validated_data
            print(from_user_data)
            # try:
            #   instence=Category_Gender.objects.get(id=from_user_data['category'])
            #   print(instence.id)
            # except Category_Gender.DoesNotExist:
            #   return Response({'error': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)
            ProductData.objects.create(productname=from_user_data['productname'],price=from_user_data['price'],offer_price=from_user_data['offer_price'],size=from_user_data['size'],item_photo=from_user_data['item_photo'],category_name=from_user_data['category_name'])
            # product = serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:  
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
      

      
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
            data = serializer.validated_data
            product.productname = data.get('productname')
            product.price = data.get('price')
            product.offer_price = data.get('offer_price')
            product.size = data.get('size')
            product.item_photo = data.get('item_photo')
            product.category_name = data.get('category_name')
            product.save()

            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
      

class PaginationApiview(APIView):
    def get(self, request, format=None):
        productdata =ProductData.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10 
        result_page = paginator.paginate_queryset(productdata, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data) 
      
    
class OrderDetails(APIView):
     def get(self,request):
        order_details=Orderitem.objects.select_related('user_forin','product').all()
        serializer=OrderDetileserializer(order_details,many=True)
        return Response(serializer.data,status=status.HTTP_302_FOUND)   