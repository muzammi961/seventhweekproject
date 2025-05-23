from django.shortcuts import render
from rest_framework.response import Response
from adminuser.models import ProductData
from authentication.models import CustomUser      
from rest_framework.permissions import AllowAny


from .serialaizer import WishListSerialaizer,ItemCartSerialaizer,WishListSerialaizer
from rest_framework.views import APIView
from .models import Cart,ItemCart,WishList,WishListUser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class AddProductCart(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user=request.user
        print(user)
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
        
class AddProductWishlist(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        print("it is the user side   ", user)
        product_id = request.data.get('product')
        print('id',product_id)
        if not product_id:
            return Response({'message': 'Product is not received'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            product = ProductData.objects.get(id=product_id)
        except ProductData.DoesNotExist:
            return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
          
        wishlist_user, created_user = WishListUser.objects.get_or_create(user=user)
        if created_user :
          message1 = "User created inside the wishlist"    
        else :
          message1 ="User already exists in wishlist"
        wishlist_item, created_wishlist = WishList.objects.get_or_create(wishuser=wishlist_user, product=product)
        if created_wishlist:
            message2 = "Product added to wishlist"
        else :
          message2="Product already in wishlist"
        return Response({'message1': message1,'message2': message2,'wishlist': WishListSerialaizer(wishlist_item).data}, status=status.HTTP_201_CREATED if created_wishlist else status.HTTP_200_OK)
      

      
class CartViewByUser(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        try:
            userobj = CustomUser.objects.get(username=user)
            print("User:", userobj.username)
        except CustomUser.DoesNotExist:
            return Response({"message": 'user does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            obj2 = ItemCart.objects.select_related('product').filter(cart__user=userobj)
            for i in obj2:
                print(i.id, i.product.productname)
            serializer = ItemCartSerialaizer(obj2, many=True)
        except ItemCart.DoesNotExist:
            return Response({'message': 'ItemCart does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)  
      
      
class WishListViewByUser(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        try:
            userobj = CustomUser.objects.get(username=user)
            print("User:", userobj.username)
        except CustomUser.DoesNotExist:
            return Response({"message": 'user does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            obj2 = WishList.objects.select_related('product').filter(wishuser__user=userobj)
            for i in obj2:
                print(i.id, i.product.productname)
            serializer = WishListSerialaizer(obj2, many=True)
        except ItemCart.DoesNotExist:
            return Response({'message': 'ItemCart does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)  
            