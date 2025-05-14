from django.urls import path
from .views import UserRegisteration,UserLogin,UserLogout,ChangePasswordAPIView
from . import views
urlpatterns = [
    path('userregisteration/',UserRegisteration.as_view()),
    path('UserLogin/',UserLogin.as_view()),
    path('UserLogout/',UserLogout.as_view()),
    path('ChangePasswordAPIView/',ChangePasswordAPIView.as_view())
    
    
]
