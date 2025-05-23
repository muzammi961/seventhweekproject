from django.urls import path
from .views import AddProductCart,AddProductWishlist,CartViewByUser,WishListViewByUser
urlpatterns = [
    path('AddProductCart/',AddProductCart.as_view()),
    path('AddProductWishlist/',AddProductWishlist.as_view()),
    path('CartViewByUser/',CartViewByUser.as_view()),
    path('WishListViewByUser/',WishListViewByUser.as_view())
]
