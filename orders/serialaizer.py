from rest_framework.serializers import Serializer
from rest_framework.serializers import ModelSerializer
from .models import Orderusre,Orderitem

from rest_framework import serializers
from products.serialaizer import ViewProductsByCategorySerialaizer
from authentication.serializer import CustomUserSerializer
from .models import Orderitem

class OrderUserSerialaizer(ModelSerializer):
    class Meta:
        model=Orderusre
        fields='__all__'


class OrderProductSerialaizer(ModelSerializer):
    class Meta:
        model=Orderitem
        fields='__all__'      
    
    

class OrderDetileserializer(serializers.ModelSerializer):
    product = ViewProductsByCategorySerialaizer(read_only=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = Orderitem
        fields = ['user', 'product', 'quantity', 'ordered_at']

    def get_user(self, obj):
        return CustomUserSerializer(obj.user_forin.user).data
