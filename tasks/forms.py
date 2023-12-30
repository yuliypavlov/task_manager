"""
This module contains the forms for the tasks application.
It includes a form for creating a task and a form for registering a new user.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from tasks.models import Task


class TaskForm(forms.ModelForm):
    """
    Form for creating a new task.
    The form includes fields for the task's title and description.
    """
    class Meta:
        model = Task
        fields = ['title', 'description']


class RegistrationForm(UserCreationForm):
    """
    Form for registering a new user.
    The form includes fields for the user's username, email, and password.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        """
        Save the form data to the User model.
        The email field is added to the saved user instance.
        """
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
