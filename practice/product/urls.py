from django.urls import path, include
from . import views
from .views import ProductAPI
#from myproject.customer import views
from rest_framework.routers import DefaultRouter
from .views import ProductAPI

urlpatterns = [
    path('',ProductAPI.as_view(),name='root'),
    path('customer/',views.ProductAPI.as_view(),name='api'),
    path('<int:id>/',ProductAPI.as_view(),name='details'),
]