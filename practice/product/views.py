from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from .models import Product
from .serializers import ProductSerializer

# Create your views here.
class ProductAPI(APIView):
    def post(self,request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,stats=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,id=None):
        if id:
            try:
                product = Product.object.get(id=id)
            except Product.DoesNotExist:
                return Response({"error":"Not Found"},status=status.HTTP_404_NOT_FOUND)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many = True)
        return Response(serializer.data)
    
    def put(self,request,id):
        if id:
            try:
                product = Product.object.get(id=id)
            except Product.DoesNotExist:
                return Response({"error":"Not Found"},status.HTTP_404_NOT_FOUND)
            
            serializer = ProductSerializer(product, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        try:
            product = Product.object.get(id=id)
        except Product.DoesNotExist:
            return Response({"error":"Not Found"},status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response({"message":"Deleted"},status=status.HTTP_204_NO_CONTENT)