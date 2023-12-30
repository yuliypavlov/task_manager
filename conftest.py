"""
This module contains pytest fixtures for the 'tasks' application.

It includes fixtures for creating a user, an author, an author client
and a task.
"""

from datetime import datetime

import pytest

from tasks.models import Task


@pytest.fixture
def user(client, django_user_model):
    """
    Pytest fixture for creating a user and logging them in.
    """
    user = django_user_model.objects.create_user(username='user')
    client.force_login(user)
    return client


@pytest.fixture
def author(django_user_model):
    """
    Pytest fixture for creating an author.
    """
    return django_user_model.objects.create(username='author')


@pytest.fixture
def author_client(client, author):
    """
    Pytest fixture for creating an author client and logging them in.
    """
    client.force_login(author)
    return client


@pytest.fixture
def task(db, author):
    """
    Pytest fixture for creating a task.
    """
    return Task.objects.create(
        title='Test task', description='Test description',
        created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        updated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        author=author)
