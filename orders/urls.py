from django.urls import path
from .views import OrderProductView,OrderDetailView
urlpatterns = [
    path('OrderProduct/',OrderProductView.as_view()),
    path('OrderDetile/',OrderDetailView.as_view())
]
