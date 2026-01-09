from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from .models import User
from .serializers import UserSerializer
# Import this for the login check
from django.contrib.auth.hashers import check_password

class UserAPI(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # If adding fails, this will return the exact reason (e.g., "Email already exists")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id:
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                return Response({'error': "Not Found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = UserSerializer(user)
            return Response(serializer.data)

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def put(self, request, id=None):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'error': "Not Found"}, status=status.HTTP_404_NOT_FOUND)

        # Added partial=True so you don't HAVE to send the password every time you update a name/phone
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)
            user.delete()
            return Response({"message": "User Deleted"}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'error': "Not Found"}, status=status.HTTP_404_NOT_FOUND)

class LoginAPI(APIView):
    def post(self, request):
        # GET DATA MANUALLY - Do NOT use UserSerializer here
        email = request.data.get('email')
        password = request.data.get('password')

        print(f"DEBUG: Email: {email}, Password: {password}") # Check your terminal for this!

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=400)

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                return Response({
                    "message": "Login successful",
                    "user": {"id": user.id, "name": user.name, "email": user.email}
                }, status=200)
            return Response({"error": "Invalid credentials"}, status=401)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)