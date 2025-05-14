from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
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