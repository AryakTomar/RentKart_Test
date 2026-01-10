from rest_framework import serializers
from .models import Customer # Make sure to import your model

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer  # This is the missing piece
        fields = '__all__' # Or a list of specific fields like ['id', 'name']