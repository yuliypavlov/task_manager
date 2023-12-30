"""
This module contains serializers for the 'tasks' application.
It includes serializers for the User and Task models.
"""

from rest_framework import serializers
from django.contrib.auth.models import User

from tasks.models import Task


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        ref_name = 'APIUser'


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.
    """
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Task
        fields = ['id', 'title', 'created_at', 'updated_at', 'description',
                  'completed', 'author']
        read_only_fields = ['author']
