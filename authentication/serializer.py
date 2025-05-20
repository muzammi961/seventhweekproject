from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.core.mail import send_mail,BadHeaderError
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from .models import CustomUser
class RegisterUserSerializer(ModelSerializer):
       password_two=serializers.CharField()
       class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password_two'] 
       
       def validate(self,data):
              if data['password'] != data['password_two']:
                  raise serializers.ValidationError('password does not match')
              return data
       def create(self, validated_data):
              validated_data.pop('password_two')
              validated_data['password']=make_password(validated_data['password'])
              return CustomUser.objects.create(**validated_data)
          
          
class LoginSerializers(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
    
    def validate(self, data):
        user = authenticate(**data)
        if not user:
            raise AuthenticationFailed('User credentials are not correct')
        return {'user': user}
    
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True) 
    
    


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def validate_email(self, value):
        try:
            user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

        user.otp_generate()
        try:
            send_mail(
                subject="Password Reset OTP ....",
                message=f"Your OTP is for password reset :: {user.otp}",
                from_email="muzammil2332005@gmail.com.....",
                recipient_list=[user.email],
                fail_silently=False,
            )
        except BadHeaderError:
            raise serializers.ValidationError("Invalid header found.")
        except Exception as e:
            raise serializers.ValidationError("Failed to send email. Please try again later.")
        return value


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()

    def validate(self, data):
        try:
            user = CustomUser.objects.get(email=data["email"])
            if user.otp != data["otp"]:
                raise serializers.ValidationError({"otp": "Invalid OTP."})
            if timezone.now() >= user.otp_expiration:
                raise serializers.ValidationError({"otp": "OTP has expired."})
            user.otp_varified = True
            user.save()
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"email": "User not found."})
        return data



class PasswordResetSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()
    conform_password=serializers.CharField()

    def validata(self,data):
        if data['password'] != data['conform_password']:
           raise serializers.ValidationError('password does not match ..')
        try:
            user=CustomUser.objects.get(email=data['email'])
            if not user.otp_varified:
                raise serializers.ValidationError({"otp":"OTP Verification Required."})
            
        except CustomUser.DoesNotExist:     
             raise  serializers.ValidationError({"email":"email is not found..."})
        return data
    def save(self,**_data):
        user=CustomUser.objects.get(email=self.validated_data['email'])
        user.set_password(self.validated_data['password'])
        user.otp=None
        user.otp_expiration=None
        user.otp_varified=False
        user.save()
        return user