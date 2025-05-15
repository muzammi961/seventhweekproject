from django.urls import path
from .views import AddProductCart,AddProductWishlist
urlpatterns = [
    path('AddProductCart/',AddProductCart.as_view()),
    path('AddProductWishlist/',AddProductWishlist.as_view())
]
