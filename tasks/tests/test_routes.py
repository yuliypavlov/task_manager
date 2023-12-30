"""
This module contains tests for the URL routes in the 'tasks' application.
It includes tests for both anonymous and authenticated users,
and checks for correct HTTP status codes and redirects.
"""

from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from django.urls import reverse

TASK_ID = 1


@pytest.mark.parametrize(
    'url_name, expected_status',
    [('tasks:task_list', HTTPStatus.OK),
     ('tasks:login', HTTPStatus.OK),
     ('tasks:register', HTTPStatus.OK)])
def test_anonymous_user_access(client, url_name, expected_status, task):
    """
    Test that an anonymous user gets the expected HTTP status code
    when accessing various URLs.
    """
    url = reverse(url_name)

    response = client.get(url)

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url_name, expected_status, arg',
    [('tasks:task_create', HTTPStatus.OK, None),
     ('tasks:task_update', HTTPStatus.OK, TASK_ID),
     ('tasks:task_delete', HTTPStatus.OK, TASK_ID),
     ('tasks:user_profile', HTTPStatus.OK, 'username'),
     ('tasks:user_profile_update', HTTPStatus.OK, 'username')])
def test_authenticated_author_access(
        author_client, author, task, url_name, arg, expected_status):
    """
    Test that an authenticated author gets the expected HTTP status code
    when accessing various URLs.
    """
    args = (arg,) if arg else ()
    if 'user' in url_name:
        args = (author.username,)
    url = reverse(url_name, args=args)

    response = author_client.get(url)

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url_name, expected_status, arg',
    [('tasks:task_update', HTTPStatus.FORBIDDEN, TASK_ID),
     ('tasks:task_delete', HTTPStatus.FORBIDDEN, TASK_ID)])
def test_authenticated_user_access(
        user, task, url_name, arg, expected_status):
    """
    Test that an authenticated user gets the expected HTTP status code
    when accessing various URLs.
    """
    url = reverse(url_name, args=(arg,))

    response = user.get(url)

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url_name, arg',
    [('tasks:task_create', None),
     ('tasks:task_update', TASK_ID),
     ('tasks:task_delete', TASK_ID)])
def test_anonymous_user_redirect(client, url_name, arg, task):
    """
    Test that an anonymous user is redirected to the login page
    when trying to access certain URLs.
    """
    args = (arg,) if arg else ()
    url = reverse(url_name, args=args)

    response = client.get(url)
    expected_url = f"{reverse('tasks:login')}?next={url}"

    assertRedirects(response, expected_url)
