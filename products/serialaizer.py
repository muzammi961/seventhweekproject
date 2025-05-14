from rest_framework import serializers
from adminuser.models import ProductData

class ViewProductsByCategorySerialaizer(serializers.ModelSerializer):
    class Meta:
        model=ProductData
        fields ='__all__'
