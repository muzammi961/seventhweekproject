from rest_framework import serializers
from authentication.models import CustomUser
from .models import ProductData,Category_Gender
class AdminViewallUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields = ['id','username', 'email'] 


class ProductSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category_Gender.objects.all(),source='category_name',write_only=True)
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProductData
        fields = ['id', 'productname', 'price', 'offer_price', 'size', 'item_photo', 'category', 'category_id']
        # fields='__all__'  