"""
This module contains the viewsets for the 'api' application.
It includes a viewset for interacting with User objects
and a viewset for interacting with Task objects.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from tasks.models import Task
from api.serializers import UserSerializer, TaskSerializer
from api.permissions import IsAuthor
from api.pagination import TaskPagination


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing User instances.
    Only authenticated users can interact with this viewset.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAuthenticated]


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Task instances.
    Only the author of a task
    or an authenticated user can interact with this viewset.
    The tasks are paginated using the TaskPagination class.
    """
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsAuthor]
    pagination_class = TaskPagination

    def perform_create(self, serializer):
        """
        Override the perform_create method to associate the logged in user
        as the author of the task.
        """
        serializer.save(author=self.request.user)
