from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        models = Customer
        fields = "__all__"
