from django.urls import path
from .views import OrderProductView,OrderDetailView,OrderOneProductView,UserformAddress,UseraddressGet,UpdateUserAddress,OrderProductformHomeandProduct
# ,GetOrderProductOneByOne
urlpatterns = [
    path('OrderProduct/',OrderProductView.as_view()),
    path('OrderDetile/',OrderDetailView.as_view()),
    path('OrderOneProductView/<int:pk>/',OrderOneProductView.as_view()),
    path('UserformAddress',UserformAddress.as_view()),
    path('UseraddressGet',UseraddressGet.as_view()),
    # path('GetOrderProductOneByOne/<int:pk>/',GetOrderProductOneByOne.as_view())
    path('UpdateUserAddress/',UpdateUserAddress.as_view()),
    path('OrderProductformHomeandProduct/',OrderProductformHomeandProduct.as_view())
]
