from django.urls import path, include
from . import views
from .views import SubscribeAPI
#from myproject.customer import views
from rest_framework.routers import DefaultRouter
from .views import SubscribeAPI

urlpatterns = [
    path('',SubscribeAPI.as_view(),name='root'),
    path('subscription/',views.SubscribeAPI.as_view(),name='api'),
    path('<int:id>/',SubscribeAPI.as_view(),name='details'),
]