from django.urls import path
from .views import AddProductCart,AddProductWishlist,CartViewByUser,WishListViewByUser,UpdatetheQuantity,DeletetheWishListOneByOne
urlpatterns = [
    path('AddProductCart/',AddProductCart.as_view()),
    path('AddProductWishlist/',AddProductWishlist.as_view()),
    path('CartViewByUser/',CartViewByUser.as_view()),
    path('WishListViewByUser/',WishListViewByUser.as_view()),
    path('UpdatetheQuantity/<int:pk>/',UpdatetheQuantity.as_view()),
    path('DeletetheWishListOneByOne/<int:pk>/',DeletetheWishListOneByOne.as_view())
]
