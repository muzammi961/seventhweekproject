from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Cart, Orderitem, Orderusre,Useraddressuser,Useraddress
from cart.models import ItemCart
from adminuser.models import ProductData  
from authentication.models import CustomUser  
from .serialaizer import OrderDetileserializer,UseraddressuserSerializer,UseraddressSerializer,OrderProductSerialaizer

class OrderProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        print("user id:", user.id)

        try:
            cart = Cart.objects.get(user=user)
            print("Cart found for user:", cart.user)
        except Cart.DoesNotExist:
            return Response({"detail": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

        cart_items = ItemCart.objects.filter(cart=cart)
        if not cart_items.exists():
            return Response({"detail": "Your cart is empty"}, status=status.HTTP_404_NOT_FOUND)
        order_user, created = Orderusre.objects.get_or_create(user=user)
        if created:
            print("New Orderusre created.")
        else:
            print("Orderusre already exists.")
        for item in cart_items:
            Orderitem.objects.create(user_forin=order_user,product=item.product,quantity=item.quantity)
        cart_items.delete()
        cart.delete()

        return Response({"detail": "Order placed successfully and order cleared."}, status=status.HTTP_201_CREATED)



class OrderOneProductView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,pk):
        user=request.user
        print('user name ',user.id)
        try:
            cart=Cart.objects.get(user=user)
            print('cart found for user',cart.user)
        except Cart.DoesNotExist:
            return Response({'error':'cart does not existed...'})    
        try:
          cart_items=ItemCart.objects.select_related('product').filter(cart=cart,product__id=pk)
          print('items in you cards.....',cart_items)
        except ItemCart.DoesNotExist:
            print('item does not existed')
            return Response({'error':'item does not existed...'})
        if not cart_items.exists():
            return Response({'error': 'No matching item in cart for this product.'}, status=404)
        order_user, created = Orderusre.objects.get_or_create(user=user)
        if created:
            print("New Orderusre created.")
        else:
            print("Orderusre already exists.")
        for item in cart_items:
            Orderitem.objects.create(user_forin=order_user,product=item.product,quantity=item.quantity)
            print('itemss....',item.product,item.quantity)
        cart_items.delete()
        return Response({"detail": "Order placed successfully and order cleared."}, status=status.HTTP_201_CREATED)




       
class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        orders = Orderitem.objects.filter(user_forin__user=user).select_related('user_forin__user', 'product')
        serializer = OrderDetileserializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
    
class UserformAddress(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        user=request.user
        print(user)
        try:
           username=CustomUser.objects.get(username=user)
        except CustomUser.DoesNotExist:
           return Response({'message':'user does not get....'},status=status.HTTP_404_NOT_FOUND)
        try:
           get_user,creat=Useraddressuser.objects.get_or_create(username=username)
        except Useraddressuser.DoesNotExist:
            return Response({"message":'you got unexpted error ..'})   
        if creat:
            return Response({'message':"new user created..."},status=status.HTTP_200_OK)
        if Useraddress.objects.filter(adduser=get_user).exists():
            return Response({'message':'this address user alredy added ..'},status=status.HTTP_400_BAD_REQUEST)
        try:
            data=request.data
            print(data.get('nameofuser'))
            print(data.get('phonenumber'))
            print(data.get('pincode'))
            print(data.get('state'))
            print(data.get('city'))
            print(data.get('houseno_buildingname'))
            print(data.get('Roadname'))
            gettheaddress,createdform=Useraddress.objects.get_or_create(nameofuser=data.get('nameofuser'),phonenumber=int(data.get('phonenumber')), pincode=int(data.get('pincode')),state=data.get('state'),city=data.get('city'),houseno_buildingname=data.get('houseno_buildingname'),Roadname=data.get('Roadname'),adduser=get_user)
            return Response({'message':"the address form successfully"},status=status.HTTP_201_CREATED)
        except Useraddress.DoesNotExist:
            return Response({'message':"Erron while create the address"},status=status.HTTP_400_BAD_REQUEST)
                   
class UseraddressGet(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        print('user name',request.user)
        try:
            get_user = Useraddressuser.objects.get(username=user)
            print('user name...',get_user.username)
        except Useraddressuser.DoesNotExist:
            return Response({'message': 'User not found'})
        try:
            getthedata = Useraddress.objects.filter(adduser=get_user)
            # print('getthe data ....',getthedata)
            # for i in getthedata:
            #     print(i.nameofuser, i.phonenumber, i.pincode)
            serializer = UseraddressSerializer(getthedata,many=True)
            print(serializer.data)
        except Useraddress.DoesNotExist:
            return Response({"message": 'Address data not found'})
        return Response(serializer.data,status=status.HTTP_200_OK)




# class GetOrderProductOneByOne(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, pk):
#         user = request.user
#         print('user  ...', user)

#         order_items = Orderitem.objects.select_related('user_forin', 'product').filter(
#             Q(user_forin__user=user) & Q(product__id=pk)
#         )

#         if not order_items.exists():
#             return Response({'message': 'No matching data found'}, status=404)
#         item = order_items[0]
#         data = {
#             'productname': item.product.productname,
#             'price': item.product.price,
#             'offer_price': item.product.offer_price,
#             'item_photo': item.product.item_photo.url if item.product.item_photo else None,
#             'quantity': item.quantity
#         }       

#         return Response({
#             'message': 'got datas',
#             'data': data
#         })



class UpdateUserAddress(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        user = request.user
        try:
            userobj = Useraddress.objects.get(adduser__username=user)
        except Useraddress.DoesNotExist:
            return Response({'message': 'Address not found.'}, status=404)
        serializer = UseraddressSerializer(userobj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Address updated successfully.'})
        return Response(serializer.errors, status=400)
    
    


# class OrderProductformHomeandProduct(APIView):
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         user = request.user
#         order_user, created = Orderusre.objects.get_or_create(user=user)
#         print('user names ....',order_user,'  created              ...',created)
#         if created:
#             print('New Orderusre created...')
#         else:
#             print("Orderusre already exists.")

#         serializer = OrderProductSerialaizer(data=request.data, many=True)

#         if serializer.is_valid():
#             validated_data = serializer.validated_data
#             # print(validated_data) 
#             # for item in validated_data:
#             #     product = item['product']
#             Orderitem.objects.create(user_forin=order_user, product=validated_data.get('product'))
#             return Response({"message": "Order completed successfully!"})
#         else:
#             return Response({'message': 'Validation failed','errors': serializer.errors}, status=400)



class OrderProductformHomeandProduct(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        order_user, created = Orderusre.objects.get_or_create(user=user)
        print('user name:', order_user, ' created:', created)
        serializer = OrderProductSerialaizer(data=request.data, many=True)

        if serializer.is_valid():
            validated_data = serializer.validated_data

            for item in validated_data:
                product = item['product']
                quantity = item.get('quantity', 1)  
                Orderitem.objects.create(user_forin=order_user,product=product,quantity=quantity)
            return Response({"message": "Order placed successfully!"})
        else:
            return Response({'message': 'Validation failed', 'errors': serializer.errors},status=400)
