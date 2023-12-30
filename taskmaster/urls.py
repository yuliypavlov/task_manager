"""
This module defines the main URL configurations for the project.
It includes paths for the admin site, the 'tasks' application,
the 'api' application, and the API documentation.
The API documentation is generated using the drf_yasg library.
"""

from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title='Task Manager',
      default_version='v1',
      description='API documentation for Task Manager',
      terms_of_service='https://www.TaskManager.com/policies/terms/',
      contact=openapi.Contact(email='contact@task_manager.local'),
      license=openapi.License(name='BSD License'),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls', namespace='tasks')),
    path('api/v1/', include('api.urls', namespace='api')),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
]
