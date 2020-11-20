from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from acetoon_backend.views import *

router = DefaultRouter()
router.register(r'profile', UserNavView, basename='profile')
router.register(r'users', UserCreateViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
