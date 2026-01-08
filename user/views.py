from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from .models import User
from .serializers import UserSerializer

# Create your views here.
class UserAPI(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,id=None):
        if id:
            try:
                customer = User.objects.all(id=id)
            except User.DoesNotExist:
                return Response({"error":"Not Found"},status=status.HTTP_404_NOT_FOUND)
            
            serializer = UserSerializer(customer)
            return Response(serializer.data)
        
        users = User.objects.all()
        serializer = UserSerializer(users, many = True)
        return Response(serializer.data)
    
    def put(self,request,id):
        if id:
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                return Response({"error":"Not Found"},status=status.HTTP_404_NOT_FOUND)
            
            serializer = UserSerializer(user, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"error":"Not Found"},status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({"message":"Deleted"},status=status.HTTP_204_NO_CONTENT)