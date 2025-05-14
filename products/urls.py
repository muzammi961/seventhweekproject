from django.urls import path
from .views import ViewProductsByCategory,ViewSpecificProduct

urlpatterns = [
    path('ViewProductsByCategory/<str:bycategory>/',ViewProductsByCategory.as_view()),
    path('ViewSpecificProduct/<int:pk>/',ViewSpecificProduct.as_view())
]
