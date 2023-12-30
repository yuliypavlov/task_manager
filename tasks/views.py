"""
This module contains the views for the tasks application.
It includes views for registering a user, viewing and updating a user profile,
and creating, updating, deleting and listing tasks.
"""

from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DetailView, UpdateView,
                                  DeleteView, ListView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.db.models import Q

from tasks.models import Task
from tasks.forms import TaskForm, RegistrationForm


class TaskAuthorMixin(UserPassesTestMixin):
    """
    Mixin used to ensure that a task can only be updated
    or deleted by its author.
    """
    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author


class RegistrationView(CreateView):
    """
    View for registering a new user.
    """
    form_class = RegistrationForm
    template_name = 'registration/register.html'

    def get_success_url(self):
        return reverse_lazy('tasks:login')


class UserProfileView(LoginRequiredMixin, DetailView):
    """
    View for displaying a user's profile.
    """
    model = User
    template_name = 'tasks/user_profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin,
                            UpdateView):
    """
    View for updating a user's profile.
    """
    model = User
    form_class = UserChangeForm
    template_name = 'tasks/user_profile_update.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_success_url(self):
        return reverse_lazy('tasks:user_profile',
                            kwargs={'username': self.request.user.username})

    def test_func(self):
        profile_user = self.get_object()
        return self.request.user == profile_user


class TaskCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new task.
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(TaskAuthorMixin, UpdateView):
    """
    View for updating an existing task.
    """
    model = Task
    template_name = 'tasks/task_update.html'
    fields = ['title', 'description', 'completed']


class TaskDeleteView(TaskAuthorMixin, DeleteView):
    """
    View for deleting a task.
    """
    model = Task
    template_name = 'tasks/task_delete.html'

    def get_success_url(self):
        return reverse('tasks:task_list')


class TaskListView(ListView):
    """
    View for listing all tasks for the current user.
    """
    model = Task
    template_name = 'tasks/task_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(author=self.request.user)
            # Get the query parameters for filtering and sorting
            search_query = self.request.GET.get('search', '')
            sort_by = self.request.GET.get('sort_by', '-created_at')
            if search_query:
                queryset = queryset.filter(
                    Q(title__icontains=search_query) |
                    Q(description__icontains=search_query))
            if sort_by in ['-created_at', '-updated_at', '-completed']:
                queryset = queryset.order_by(sort_by)
        else:
            queryset = Task.objects.none()
        return queryset
