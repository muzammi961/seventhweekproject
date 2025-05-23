from django.urls import path
from .views import AdminViewallUser,ViewSpecificUserDetails,CreateProductView,GetallProducts,ViewAllProductbyCategory,UpdateProductView,DeleteaProduct,PaginationApiview,OrderDetails
from . import views
urlpatterns = [
   path('AdminViewallUser/',AdminViewallUser.as_view()),
   path('ViewSpecificUserDetails/<int:pk>/',ViewSpecificUserDetails.as_view()),
   path('CreateProduct/',CreateProductView.as_view()),
   path('GetallProducts/',GetallProducts.as_view()),
   path('ViewAllProductbyCategory/<str:valuebycategory>/',ViewAllProductbyCategory.as_view()) ,
   path('DeleteaProduct/<int:pk>/',DeleteaProduct.as_view()), 
   path('UpdateProductView/<int:pk>/',UpdateProductView.as_view()),
   path('PaginationApiview/',PaginationApiview.as_view()),
   path('OrderDetails/',OrderDetails.as_view())
]
