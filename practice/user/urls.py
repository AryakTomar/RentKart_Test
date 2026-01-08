from django.urls import path
from . import views
#from rest_framework.routers import DefaultRouter
from .views import UserAPI

#router = DefaultRouter()
#outer.register(r'user',UserAPI)

urlpatterns = [
    path('',UserAPI.as_view(), name = 'root'),
    path('user/',views.UserAPI.as_view(), name = 'user_api'),
    path('<int:id>/',UserAPI.as_view(), name = 'detail'),
]

