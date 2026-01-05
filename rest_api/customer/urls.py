from django.contrib import admin
from django.urls import path
from .views import CustomerAPI
from rest_api.customer import views

urlpatterns = [
    path("",views.CustomerAPI.as_view())
]