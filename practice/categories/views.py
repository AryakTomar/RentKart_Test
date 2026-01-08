from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from .models import Category
from .serializers import CategorySerializer

class CategoryAPI(APIView):
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # Fixed 'stats' typo
    
    def get(self, request, id=None):
        if id:
            try:
                # Fixed 'object' to 'objects'
                category = Category.objects.get(id=id) 
            except Category.DoesNotExist:
                return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def put(self, request, id):
        try:
            category_instance = Category.objects.get(id=id) # Fixed 'object'
        except Category.DoesNotExist:
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Ensure we pass the instance to the serializer
        serializer = CategorySerializer(category_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            category_instance = Category.objects.get(id=id) # Fixed 'object'
            category_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)