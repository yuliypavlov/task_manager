"""
This module defines the URL routes for the 'api' application.

The routes are defined using a combination of Django's path function
and Django Rest Framework's DefaultRouter.
The DefaultRouter automatically generates the URL routes for the UserViewSet
and TaskViewSet viewsets.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import UserViewSet, TaskViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
