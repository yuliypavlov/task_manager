"""
This module defines the URL configurations for the 'tasks' application.
"""

from django.urls import path
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)

from tasks.views import (TaskCreateView, TaskUpdateView, TaskDeleteView,
                         TaskListView, RegistrationView, UserProfileView,
                         UserProfileUpdateView)

app_name = 'tasks'

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('update/<int:pk>/', TaskUpdateView.as_view(), name='task_update'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='task_delete'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(next_page='tasks:task_list'),
         name='login'),
    path('user/<str:username>/', UserProfileView.as_view(),
         name='user_profile'),
    path('user/<str:username>/update/', UserProfileUpdateView.as_view(),
         name='user_profile_update'),
    path('logout/', LogoutView.as_view(next_page='tasks:task_list'),
         name='logout'),
    path('password_change/', PasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(),
         name='password_change_done'),
]
