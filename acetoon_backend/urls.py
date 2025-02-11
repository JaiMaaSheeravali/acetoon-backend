from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from acetoon_backend.views import *

router = DefaultRouter()
router.register(r'profile', UserNavView, basename='profile')
router.register(r'users', UserCreateViewSet, basename='users')
router.register(r'contests', ContestDetail, basename='contest')
router.register(r'create_contest', ContestCreate, basename='contest_create')
router.register(r'be_a_organizer', CreateOrganizer, basename='be_a_organizer')
router.register(r'team', TeamCreateViewSet, basename='team')
router.register(r'submissions', SubmissionViewSet, basename='submissions')
router.register(r'announcements', AnnouncementViewSet, basename='announcements')

urlpatterns = [
    path('', include(router.urls)),
]
