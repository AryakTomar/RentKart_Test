from django.urls import path, include
from . import views
from .views import CategoryAPI
#from myproject.customer import views
from rest_framework.routers import DefaultRouter
from .views import CategoryAPI

urlpatterns = [
    path('',CategoryAPI.as_view(),name='root'),
    path('categories/',views.CategoryAPI.as_view(),name='api'),
    path('<int:id>/',CategoryAPI.as_view(),name='details'),
]