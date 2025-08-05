from django.urls import path
from .views import AdminViewallUser,ViewSpecificUserDetails,CreateProductView,GetallProducts,ViewAllProductbyCategory,UpdateProductView,DeleteaProduct,PaginationApiview,OrderDetails,GetallCategory,GetSpecificProduct,CreateCategory,DeleteCategory,UpdateCategory,Updateuserdata,Deleteuserdata,OrderDetailsBYuser,GetAddressBYUser,Dashboardstats
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
   path('OrderDetails/',OrderDetails.as_view()),
   path('GetallCategory/',GetallCategory.as_view()),
   path('GetSpecificProduct/<int:pk>/',GetSpecificProduct.as_view()),
   path('CreateCategory/',CreateCategory.as_view()),
   path('DeleteCategory/<int:pk>/',DeleteCategory.as_view()),
   path('UpdateCategory/<int:pk>/',UpdateCategory.as_view()),
   path('Updateuserdata/<int:pk>/',Updateuserdata.as_view()),
   path('Deleteuserdata/<int:pk>/',Deleteuserdata.as_view()),
   path('OrderDetailsBYuser/<int:pk>/',OrderDetailsBYuser.as_view()),
   path('GetAddressBYUser/<int:pk>/',GetAddressBYUser.as_view()),
   path('Dashboardstats/',Dashboardstats.as_view())
]
