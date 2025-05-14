from django.urls import path
from .views import AddProductCart
urlpatterns = [
    path('AddProductCart/',AddProductCart.as_view())
]
