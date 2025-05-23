from tokenize import TokenError
from django.shortcuts import render
from .serializer import ChangePasswordSerializer, RegisterUserSerializer,LoginSerializers,PasswordResetRequestSerializer,OTPVerificationSerializer,PasswordResetSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from .models import CustomUser
# Create your views here.

class UserRegisteration(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        serializer=RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
           data=serializer.validated_data
           data.pop('password_two')
           data['password']=make_password(data['password'])
           CustomUser.objects.create(username=data['username'],email=data['email'],password=data['password']) 
        #    serializer.save()
           return Response({'message':'user registered successfully ........ '},status=status.HTTP_201_CREATED)
        else:
           return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
class UserLogin(APIView):    
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializers(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            if user.is_superuser:
                refresh = RefreshToken.for_user(user)
                return Response({'message': 'Admin logged in successfully.','refresh': str(refresh),'access': str(refresh.access_token)})
            elif user:
                refresh = RefreshToken.for_user(user)
                return Response({'message': 'User logged in successfully.','refresh': str(refresh),'access': str(refresh.access_token)})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh", None)

        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError as e:
            return Response({"error": "invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        



class ChangePasswordAPIView(APIView) :
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        user = request.user
        print("tt is the user name ;;;;",user)
        if serializer.is_valid():
            if not check_password(serializer.data.get("old_password"), user.password):
                return Response({"error": "wrong old password"}, status=status.HTTP_400_BAD_REQUEST)
            new_password=serializer.data.get('new_password')
            # user.set_password(serializer.data.get("new_password"))
            # user.save()
            try:
               CustomUser.objects.filter(username__exact=user).update(password=make_password(new_password))
            except CustomUser.DoesNotExist:
                return Response({'message':"user does not existed ......"})      
            return Response({"message": "password changed successfully"})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
            
            
            
class PasswordResetRequest(APIView):
    def post(self,request):
      print(request.data)
      serializer=PasswordResetRequestSerializer(data=request.data)
      if serializer.is_valid():
          return Response({"message":"OTP  Verified"},status=status.HTTP_200_OK)
      return Response(status=status.HTTP_400_BAD_REQUEST)
  
  
class OTPVerificationView(APIView):
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "OTP verified."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
                     
                     

class PasswordResetView(APIView):
    def post(self,request):
        serializer=PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            password=make_password(serializer.validated_data['password'])
            CustomUser.objects.filter(email__exact=serializer.validated_data['email']).update(password=password,otp=None,otp_expiration=None,otp_varified=False)
            # user.set_password(self.validated_data['password'])
            # user.otp=None
            # user.otp_expiration=None
            # user.otp_varified=False
            # serializer.save()
            return Response({'message':"Password reset successfull."},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)