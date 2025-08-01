from rest_framework import serializers
from authentication.models import CustomUser
from .models import ProductData,Category_Product
class AdminViewallUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields = ['id','username', 'email'] 
                                                  

class ProductSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category_Product.objects.all(),source='category_name',write_only=True)
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProductData
        fields = ['id', 'productname', 'price', 'offer_price', 'item_photo', 'category', 'category_id']
        # fields='__all__'  
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category_Product
        fields='__all__'        