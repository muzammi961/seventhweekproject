from django.urls import path
from .views import ViewProductsByCategory,ViewSpecificProduct,Viewallproduct,GetallCategory

urlpatterns = [
    path('ViewProductsByCategory/<str:bycategory>/',ViewProductsByCategory.as_view()),
    path('ViewSpecificProduct/<int:pk>/',ViewSpecificProduct.as_view()),
    path('Viewallproduct/',Viewallproduct.as_view()),
    path('GetallCategory/',GetallCategory.as_view())
]
