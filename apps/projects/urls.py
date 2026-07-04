from django.urls import path

from apps.projects.views import home, project_delete, project_edit, serve_project_game

urlpatterns = [
    path("", home, name="home"),
    path("projects/<int:pk>/game/", serve_project_game, name="project_game_root"),
    path("projects/<int:pk>/game/<path:path>", serve_project_game, name="project_game"),
    path("projects/<int:pk>/edit/", project_edit, name="project_edit"),
    path("projects/<int:pk>/delete/", project_delete, name="project_delete"),
]
