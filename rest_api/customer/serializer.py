from rest_framework import serializers
from .models import Customer

class Customer(serializers.ModelSerializer):
    name = serializers.CharField(max_lenght = 100)
    email = serializers.EmailField(unique = True)
    phone = serializers.CharField(max_length=10)
    address = serializers.TextField(blank = True)
    created_at = serializers.DateTimeField(auto_now_add=True)

    class Meta:
        models = Customer
        fields = '__all__'