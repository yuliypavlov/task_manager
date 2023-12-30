"""
This module contains tests for the 'tasks' application.
It includes tests for task creation, update and deletion
by different types of users.
"""

import pytest
from django.urls import reverse

from tasks.models import Task


@pytest.mark.parametrize(
    'test_client, task_exists',
    [(pytest.lazy_fixture('author_client'), True),
     (pytest.lazy_fixture('client'), False)])
def test_task_creation_for_different_users(db, test_client, task_exists):
    """
    Test that tasks can be created by certain types of users.
    """
    url = reverse('tasks:task_create')
    data = {'title': 'New Task', 'description': 'Description of the new task'}

    test_client.post(url, data)

    assert Task.objects.filter(title='New Task').exists() is task_exists


@pytest.mark.parametrize(
    'test_client, can_modify',
    [(pytest.lazy_fixture('author_client'), True),
     (pytest.lazy_fixture('admin_client'), False)])
def test_task_update_by_different_users(test_client, task, can_modify):
    """
    Test that tasks can be updated by certain types of users.
    """
    url = reverse('tasks:task_update', kwargs={'pk': task.pk})
    data = {'title': 'New task', 'description': 'New description'}

    test_client.post(url, data)

    task.refresh_from_db()
    if can_modify:
        assert task.title == 'New task'
        assert task.description == 'New description'
    else:
        assert task.title == 'Test task'
        assert task.description == 'Test description'


@pytest.mark.parametrize(
    'test_client, can_modify',
    [(pytest.lazy_fixture('author_client'), True),
     (pytest.lazy_fixture('admin_client'), False)])
def test_task_delete_by_different_users(test_client, task, can_modify):
    """
    Test that tasks can be deleted by certain types of users.
    """
    url = reverse('tasks:task_delete', kwargs={'pk': task.pk})

    test_client.post(url)

    if can_modify:
        assert not Task.objects.filter(pk=task.pk).exists()
    else:
        assert Task.objects.filter(pk=task.pk).exists()
