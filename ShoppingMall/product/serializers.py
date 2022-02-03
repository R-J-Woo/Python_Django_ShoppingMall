from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    # model 연결
    class Meta:
        model = Product
        fields = '__all__'
