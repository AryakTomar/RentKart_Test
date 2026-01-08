from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from .models import Customer
from .serializers import CustomerSerializer

# Create your views here.
class CustomerAPI(APIView):
    def post(self,request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,stats=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,id=None):
        if id:
            try:
                customer = Customer.object.get(id=id)
            except Customer.DoesNotExist:
                return Response({"error":"Not Found"},status=status.HTTP_404_NOT_FOUND)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many = True)
        return Response(serializer.data)
    
    def put(self,request,id):
        if id:
            try:
                customer = Customer.object.get(id=id)
            except Customer.DoesNotExist:
                return Response({"error":"Not Found"},status.HTTP_404_NOT_FOUND)
            
            serializer = CustomerSerializer(customer, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        try:
            customer = Customer.object.get(id=id)
        except Customer.DoesNotExist:
            return Response({"error":"Not Found"},status.HTTP_404_NOT_FOUND)

        customer.delete()
        return Response({"message":"Deleted"},status=status.HTTP_204_NO_CONTENT)