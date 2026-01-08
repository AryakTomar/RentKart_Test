from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from .models import Subscribe
from .serializers import SubscribeSerializer

# Create your views here.
class SubscribeAPI(APIView):
    def post(self,request):
        serializer = SubscribeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,stats=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,id=None):
        if id:
            try:
                subscribe = Subscribe.object.get(id=id)
            except Subscribe.DoesNotExist:
                return Response({"error":"Not Found"},status=status.HTTP_404_NOT_FOUND)
            serializer = SubscribeSerializer(subscribe)
            return Response(serializer.data)
        subscriber = Subscribe.objects.all()
        serializer = SubscribeSerializer(subscriber, many = True)
        return Response(serializer.data)
    
    def put(self,request,id):
        if id:
            try:
                subscribe = Subscribe.object.get(id=id)
            except Subscribe.DoesNotExist:
                return Response({"error":"Not Found"},status.HTTP_404_NOT_FOUND)
            
            serializer = SubscribeSerializer(subscribe, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        try:
            subscribe = Subscribe.object.get(id=id)
        except Subscribe.DoesNotExist:
            return Response({"error":"Not Found"},status.HTTP_404_NOT_FOUND)

        subscribe.delete()
        return Response({"message":"Deleted"},status=status.HTTP_204_NO_CONTENT)