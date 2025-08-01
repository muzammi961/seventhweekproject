from django.urls import path
from .views import verify_payment,create_order

urlpatterns = [
    path("create-order/", create_order, name="create-order"),
    # path("create-order/", CreateOrderAPIView.as_view(), name="create-order"),
    path("verify-payment/", verify_payment, name="verify-payment"),
]
