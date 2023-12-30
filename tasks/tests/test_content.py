"""
This module contains tests for the 'tasks' application.
It includes tests for checking the task list for different users
and verifying the presence of a form in the context.
"""

import pytest
from django.urls import reverse

TASK_ID = 1


@pytest.mark.parametrize('parametrized_client, task_in_list',
                         ((pytest.lazy_fixture('author_client'), True),
                          (pytest.lazy_fixture('user'), False)))
def test_task_list_for_different_users(
        task, parametrized_client, task_in_list):
    """
    Test that the task list contains the correct tasks
    for different types of users.
    """
    url = reverse('tasks:task_list')

    response = parametrized_client.get(url)
    object_list = response.context['object_list']

    assert (task in object_list) is task_in_list


@pytest.mark.parametrize('url_name, arg',
                         [('tasks:task_create', None),
                          ('tasks:task_update', TASK_ID)])
def test_form_in_context(task, author_client, url_name, arg):
    """
    Test that a form is present in the context when accessing certain URLs.
    """
    url = reverse(url_name, args=[arg] if arg else [])

    response = author_client.get(url)

    assert 'form' in response.context
