from rest_framework import serializers
from .models import Subscribe

class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        models = Subscribe
        fields = "__all__"
