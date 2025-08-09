from django.shortcuts import render
from rest_framework.views import APIView 
from .serializer import AdminViewallUserSerializer,ProductSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from authentication.models import CustomUser
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .models import ProductData,Category_Product
from rest_framework import status
from django.http import Http404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from orders.serialaizer  import OrderDetileserializer
from orders.models import Orderitem,Orderusre      
from adminuser.serializer import ProductSerializer,CategorySerializer 
from authentication.serializer import CustomUserSerializer
from orders.serialaizer import UseraddressSerializer  
from  orders.models import Useraddressuser,Useraddress
from django.db.models import Sum, Avg, Count
from products.utils import upload_image_to_s3
# Create your views here.

class AdminViewallUser(APIView):
  permission_classes=[IsAdminUser]
  def get(self,request):
      user_data=CustomUser.objects.all()
      serializer=AdminViewallUserSerializer(user_data,many=True)
      print(serializer.data)
      return Response(serializer.data,status=status.HTTP_200_OK)
  
class ViewSpecificUserDetails(APIView):
    permission_classes=[IsAdminUser]
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
            data = serializer.validated_data

            image_file = data['item_photo']
            image_name = image_file.name

       
            image_url = upload_image_to_s3(image_file, image_name)
            print('image urls is ',image_url)
            if not image_url:
                return Response({'error': 'S3 upload failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

   
            product = ProductData.objects.create(
                productname=data['productname'],
                price=data['price'],
                offer_price=data['offer_price'],
                item_photo=image_url,  # store the URL, not the file
                category_name=data['category_name']
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


      
class GetallProducts(APIView):
  permission_classes=[IsAdminUser]
  def get(self,request):
        data=ProductData.objects.all()
        serializer=ProductSerializer(data,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
      
      

class ViewAllProductbyCategory(APIView):
    permission_classes=[IsAdminUser]
    def get(self, request, valuebycategory):
        try:
           products = ProductData.objects.filter(category_name__name=valuebycategory)
        except ProductData.DoesNotExist:
          return Response({'message':'data does noe existed....'},status=status.HTTP_400_BAD_REQUEST)
        print('productss   ....',products)
        if products.exists():
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'No products found for this category.'}, status=status.HTTP_404_NOT_FOUND)
          
          
class DeleteaProduct(APIView):
  permission_classes=[IsAdminUser]
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
            return Response({"error": "Product not found"}, 
                          status=status.HTTP_404_NOT_FOUND)
            
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, 
                          status=status.HTTP_400_BAD_REQUEST)
            
        data = serializer.validated_data
        image_url = product.item_photo  # Keep existing if no new image
        
        # Handle image update if new image provided
        if 'item_photo' in data and data['item_photo']:
            try:
                image_file = data['item_photo']
                image_name = image_file.name
                image_url = upload_image_to_s3(image_file, image_name)
                if not image_url:
                    return Response({'error': 'S3 upload failed'},
                                  status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                return Response({'error': f'Image upload error: {str(e)}'},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Update product fields
        product.productname = data.get('productname', product.productname)
        product.price = data.get('price', product.price)
        product.offer_price = data.get('offer_price', product.offer_price)
        product.item_photo = image_url
        product.category_name = data.get('category_name', product.category_name)
        product.save()

        return Response(ProductSerializer(product).data,
                      status=status.HTTP_200_OK)
      
      

class PaginationApiview(APIView):
    permission_classes=[IsAdminUser]
    def get(self, request, format=None):
        productdata =ProductData.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10 
        result_page = paginator.paginate_queryset(productdata, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data) 
      
    
# class OrderDetails(APIView):
#      permission_classes=[IsAdminUser]
#      def get(self,request):
#         order_details=Orderitem.objects.select_related('user_forin','product',).all()
#         print('order deltails .....',order_details)
#         serializer=OrderDetileserializer(order_details,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
#       return Response({'message':'data does not get'},status=status.HTTP_400_BAD_REQUEST)   
      
class OrderDetails(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            order_details = Orderitem.objects.select_related('user_forin', 'product').all()
            print('Order details:', order_details)
            serializer = OrderDetileserializer(order_details, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("Error fetching data:", e)
            return Response({'message': 'Data could not be retrieved'}, status=status.HTTP_400_BAD_REQUEST)      
      
      
      
      
class GetallCategory(APIView):
  permission_classes=[IsAdminUser]
  def get(self,request):
    try:
      getcategory=Category_Product.objects.all()
      serializer=CategorySerializer(getcategory,many=True)
    except Category_Product.DoesNotExist:
      return Response({'message':'category does not existe.....'},status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data,status=status.HTTP_200_OK)      
  
  
class GetSpecificProduct(APIView):
   permission_classes=[IsAdminUser]
   def get(self,request,pk):
     try:
       get_data=ProductData.objects.get(id=pk) 
       print('get data',get_data)
       serializer=ProductSerializer(get_data)
     except ProductData.DoesNotExist:
       return Response({'message':'data does not existed..'},status=status.HTTP_400_BAD_REQUEST)
     return Response(serializer.data,status=status.HTTP_200_OK)
   
   
class CreateCategory(APIView):
  permission_classes=[IsAdminUser]
  def post(self,request):
      serializer=CategorySerializer(data=request.data)
      if serializer.is_valid():
        data=serializer.validated_data
        Category_Product.objects.create(name=data['name'])
        return Response({'message':'category posted ...'},status=status.HTTP_200_OK)
      return Response({'message':'data does not existed....'},status=status.HTTP_400_BAD_REQUEST) 
              
              
              
class DeleteCategory(APIView):
  permission_classes=[IsAdminUser]
  def delete(self,request,pk):
      try:
        obj=Category_Product.objects.get(id=pk)
        obj.delete()
      except Category_Product.DoesNotExist:
        return Response({'message':'category does not get....!'})  
      return Response({'message':'category deleted successfully....!'})
    
    
class UpdateCategory(APIView):
   permission_classes=[IsAdminUser]
   def put(self,request,pk):
     try:
      obj=Category_Product.objects.get(id=pk)
     except Category_Product.DoesNotExist:
       return Response({'message':'category does not exist....!'})
     serializer=CategorySerializer(obj,data=request.data)
     if serializer.is_valid():
        data=serializer.validated_data
        Category_Product.objects.filter(id=pk).update(name=data.get('name'))
        return Response({'message':'category changed successfully...!'}) 
     return Response({'message':'category does not change.....'})                
            
            
            
class Updateuserdata(APIView):
    permission_classes=[IsAdminUser]
    def put(self,request,pk):
      try:
        obj=CustomUser.objects.get(id=pk)        
      except CustomUser.DoesNotExist:
        return Response({'message':'does not exist the user....!'}) 
      serializer=CustomUserSerializer(obj,data=request.data)
      if serializer.is_valid():
        data=serializer.validated_data
        CustomUser.objects.filter(id=pk).update(username=data.get('username'),email=data.get('email')) 
        return Response({'message':"user data has been changeing ...!"})
      return Response({'message':'could not update user datas....!'})
    
class Deleteuserdata(APIView):
  permission_classes=[IsAdminUser]
  def delete(self,request,pk):
    try:
      obj=CustomUser.objects.get(id=pk) 
      obj.delete()
    except CustomUser.DoesNotExist:
      return Response({'message':'user does not exist in this id...!'})
    return Response({'message':'data successfully destroyd ...!'})     
  
  
  
  
class OrderDetailsBYuser(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, pk):
        try:
            obj = Orderusre.objects.get(user__id=pk)
            print('Orderusre object:', obj)
        except Orderusre.DoesNotExist:
            return Response({'message': 'User does not exist...'}, status=status.HTTP_404_NOT_FOUND)
        data = Orderitem.objects.select_related('product').filter(user_forin=obj)
        print('Order items:', data)
        serializer = OrderDetileserializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
  


class GetAddressBYUser(APIView):
  permission_classes=[IsAdminUser]
  def get(self,request,pk):
    try:
      obj=Useraddressuser.objects.get(username__id=pk)
      print('user address id ',obj)
    except Useraddressuser.DoesNotExist:
      return Response({'message':'user address did not find..'}) 
    data=Useraddress.objects.filter(adduser=obj)
    print('order items   ...',data)
    serializer=UseraddressSerializer(data,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)
  
  


class Dashboardstats(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request): 
        total_sales = ProductData.objects.aggregate(total=Sum('offer_price'))['total'] or 0
        total_products = ProductData.objects.aggregate(count=Count('id'))['count'] or 0
        average_price = ProductData.objects.aggregate(avg=Avg('offer_price'))['avg'] or 0
        total_user = CustomUser.objects.aggregate(total=Count('id'))['total'] or 0

        data = [
            {
                "title": "Total Sales",
                "value": total_sales,
                "color": "from-purple-500 to-indigo-500",
                "icon": "🛒"
            },
            {
                "title": "Total Products",
                "value": total_products,
                "color": "from-green-500 to-teal-500",
                "icon": "📦"
            },
            {
                "title": "Average Price",
                "value": round(average_price, 2),
                "color": "from-blue-500 to-cyan-500",
                "icon": "💸"
            },
            {
                "title": "Total Users",
                "value": total_user,
                "color": "from-amber-500 to-orange-500",
                "icon": "👥"
            }
        ]

        return Response(data, status=status.HTTP_200_OK)