from django.urls import path

from apps.projects.views import home, project_delete, project_edit

urlpatterns = [
    path("", home, name="home"),
    path("projects/<int:pk>/edit/", project_edit, name="project_edit"),
    path("projects/<int:pk>/delete/", project_delete, name="project_delete"),
]
