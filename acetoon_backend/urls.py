from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from acetoon_backend.views import *

router = DefaultRouter()
router.register(r'profile', UserNavView, basename='profile')
router.register(r'users', UserCreateViewSet, basename='users')
router.register(r'contests', ContestDetail, basename='contest')
router.register(r'create_contest', ContestCreate, basename='contest_create')

urlpatterns = [
    path('', include(router.urls)),
]
