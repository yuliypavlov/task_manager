"""
This module contains the Task model for the tasks application.
"""

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Task(models.Model):
    """
    Represents a task.
    A task has a title, an optional description,
    a status indicating whether it is completed,
    timestamps for when it was created and last updated, and an author.
    The author is a foreign key to the User model,
    meaning each task is associated with a user.
    """
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tasks:task_list')
