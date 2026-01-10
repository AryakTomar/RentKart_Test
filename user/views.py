from django.shortcuts import render

# Create your views here.
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

# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status 
# from .models import User
# from .serializers import UserSerializer
# from django.contrib.auth.hashers import check_password, make_password
# from django.core.cache import cache
# import random
# import requests
# from django.conf import settings

# class UserAPI(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request, id=None):
#         if id:
#             try:
#                 user = User.objects.get(id=id)
#             except User.DoesNotExist:
#                 return Response({'error': "Not Found"}, status=status.HTTP_404_NOT_FOUND)

#             serializer = UserSerializer(user)
#             return Response(serializer.data)

#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)

#     def put(self, request, id=None):
#         try:
#             user = User.objects.get(id=id)
#         except User.DoesNotExist:
#             return Response({'error': "Not Found"}, status=status.HTTP_404_NOT_FOUND)

#         serializer = UserSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, id):
#         try:
#             user = User.objects.get(id=id)
#             user.delete()
#             return Response({"message": "User Deleted"}, status=status.HTTP_204_NO_CONTENT)
#         except User.DoesNotExist:
#             return Response({'error': "Not Found"}, status=status.HTTP_404_NOT_FOUND)


# class LoginAPI(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         print(f"DEBUG: Email: {email}, Password: {password}")

#         if not email or not password:
#             return Response({"error": "Email and password are required"}, status=400)

#         try:
#             user = User.objects.get(email=email)
#             if check_password(password, user.password):
#                 return Response({
#                     "message": "Login successful",
#                     "user": {"id": user.id, "name": user.name, "email": user.email}
#                 }, status=200)
#             return Response({"error": "Invalid credentials"}, status=401)
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=404)


# class ForgotPasswordAPI(APIView):
#     """
#     Sends OTP to user's Telegram when they request password reset
#     """
#     def post(self, request):
#         email = request.data.get('email')
        
#         if not email:
#             return Response({"error": "Email is required"}, status=400)
        
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=404)
        
#         # Generate 6-digit OTP
#         otp = str(random.randint(100000, 999999))
        
#         # Store OTP in cache with 10 minute expiration
#         cache_key = f"otp_{email}"
#         cache.set(cache_key, otp, timeout=600)  # 10 minutes
        
#         # Send OTP via Telegram
#         telegram_sent = self.send_telegram_otp(user.phone, otp, user.name)
        
#         if telegram_sent:
#             return Response({
#                 "message": "OTP sent to your Telegram successfully",
#                 "email": email
#             }, status=200)
#         else:
#             return Response({
#                 "error": "Failed to send OTP. Please ensure your phone number is linked to Telegram."
#             }, status=500)
    
#     def send_telegram_otp(self, phone, otp, name):
#         """
#         Send OTP to user via Telegram Bot
#         You need to create a Telegram Bot and get the bot token
#         """
#         try:
#             bot_token = settings.TELEGRAM_BOT_TOKEN
            
#             # Get chat_id from phone number (you'll need to maintain a mapping)
#             # For now, using phone as chat_id - you should implement proper mapping
#             chat_id = self.get_chat_id_from_phone(phone)
            
#             if not chat_id:
#                 print(f"Chat ID not found for phone: {phone}")
#                 return False
            
#             message = f"""
# 🔐 Password Reset OTP

# Hello {name}!

# Your OTP for password reset is: {otp}

# This OTP is valid for 10 minutes.

# If you didn't request this, please ignore this message.
#             """
            
#             url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
#             payload = {
#                 "chat_id": chat_id,
#                 "text": message,
#                 "parse_mode": "HTML"
#             }
            
#             response = requests.post(url, json=payload)
            
#             if response.status_code == 200:
#                 print(f"OTP sent successfully to {phone}")
#                 return True
#             else:
#                 print(f"Failed to send OTP: {response.text}")
#                 return False
                
#         except Exception as e:
#             print(f"Error sending Telegram OTP: {str(e)}")
#             return False
    
#     def get_chat_id_from_phone(self, phone):
#         """
#         Get Telegram chat_id from phone number
#         You need to implement this based on your user-telegram mapping
        
#         Option 1: Store chat_id in User model
#         Option 2: Maintain separate TelegramUser model
#         Option 3: Use cache/database mapping
#         """
#         # For now, return None - you need to implement this
#         # Example if you have chat_id in cache:
#         chat_id = cache.get(f"telegram_chat_{phone}")
#         return chat_id


# class ResetPasswordAPI(APIView):
#     """
#     Verifies OTP and resets the password
#     """
#     def post(self, request):
#         email = request.data.get('email')
#         otp = request.data.get('otp')
#         new_password = request.data.get('new_password')
        
#         if not email or not otp or not new_password:
#             return Response({"error": "All fields are required"}, status=400)
        
#         # Verify OTP
#         cache_key = f"otp_{email}"
#         stored_otp = cache.get(cache_key)
        
#         if not stored_otp:
#             return Response({"error": "OTP expired or invalid"}, status=400)
        
#         if stored_otp != otp:
#             return Response({"error": "Invalid OTP"}, status=400)
        
#         # Update password
#         try:
#             user = User.objects.get(email=email)
#             user.password = make_password(new_password)
#             user.save()
            
#             # Delete OTP from cache
#             cache.delete(cache_key)
            
#             return Response({
#                 "message": "Password reset successful"
#             }, status=200)
            
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=404)
#         except Exception as e:
#             return Response({"error": str(e)}, status=500)