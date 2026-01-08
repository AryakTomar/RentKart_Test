from django.urls import path, include
from . import views
from .views import CustomerAPI
#from myproject.customer import views
from rest_framework.routers import DefaultRouter
from .views import CustomerAPI

urlpatterns = [
    path('',CustomerAPI.as_view(),name='root'),
    path('customer/',views.CustomerAPI.as_view(),name='api'),
    path('<int:id>/',CustomerAPI.as_view(),name='details'),
]