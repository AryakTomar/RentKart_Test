from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        models = Category
        fields = "__all__"
