from django.urls import path
from .views import UserRegisteration,UserLogin,UserLogout,ChangePasswordAPIView,PasswordResetRequest,OTPVerificationView,PasswordResetView
from . import views
urlpatterns = [
    path('userregisteration/',UserRegisteration.as_view()),
    path('UserLogin/',UserLogin.as_view()),
    path('UserLogout/',UserLogout.as_view()),
    path('ChangePasswordAPIView/',ChangePasswordAPIView.as_view()),
    path('PasswordResetRequest/',PasswordResetRequest.as_view()),
    path('OTPVerificationView/',OTPVerificationView.as_view()),
    path('PasswordResetView/',PasswordResetView.as_view())
    
]
