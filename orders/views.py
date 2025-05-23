from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Cart, Orderitem, Orderusre
from cart.models import ItemCart
from adminuser.models import ProductData  
from authentication.models import CustomUser  


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
            return Response({"detail": "Your cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
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


from .serialaizer import OrderDetileserializer

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = Orderitem.objects.filter(user_forin__user=user).select_related('user_forin__user', 'product')
        serializer = OrderDetileserializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)