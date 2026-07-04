import mimetypes
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.clickjacking import xframe_options_sameorigin
from rest_framework import viewsets

from apps.projects.constants import BUILDS, CREATIVE, LIFE_OTHER
from apps.projects.forms import ProjectForm, ProjectMediaFormSet
from apps.projects.models import Project, ProjectMedia, ProjectType, Tag
from apps.projects.serializers import (
    ProjectMediaSerializer,
    ProjectSerializer,
    ProjectTypeSerializer,
    TagSerializer,
)
from apps.projects.services.game_upload import process_project_game


def _get_project_type_ids():
    types = ProjectType.objects.filter(
        name__in=[BUILDS, CREATIVE, LIFE_OTHER]
    ).values("name", "id")
    return {item["name"]: item["id"] for item in types}


def _render_home(request, form, media_formset, *, show_form=False, form_mode="add", editing_project=None):
    project_type_ids = _get_project_type_ids()
    return render(
        request,
        "pages/home.html",
        {
            "form": form,
            "media_formset": media_formset,
            "projects": Project.objects.select_related("project_type").prefetch_related("tags").order_by("title"),
            "show_form": show_form,
            "form_mode": form_mode,
            "editing_project": editing_project,
            "builds_type_id": project_type_ids.get(BUILDS),
            "creative_type_id": project_type_ids.get(CREATIVE),
            "life_type_id": project_type_ids.get(LIFE_OTHER),
        },
    )


def _save_project_with_media(form, media_formset):
    project = form.save()
    process_project_game(project)
    if not project.is_web_game:
        media_formset.instance = project
        media_formset.save()
    return project


def home(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        media_formset = ProjectMediaFormSet(request.POST, request.FILES)
        media_formset.require_media = False
        if form.is_valid() and media_formset.is_valid():
            project = _save_project_with_media(form, media_formset)
            messages.success(request, f'Project "{project.title or "Untitled"}" was created successfully.')
            return redirect("home")
        return _render_home(
            request,
            form,
            media_formset,
            show_form=True,
            form_mode="add",
        )

    show_form = request.GET.get("add") == "1"
    return _render_home(
        request,
        ProjectForm(),
        ProjectMediaFormSet(),
        show_form=show_form,
        form_mode="add",
    )


def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        media_formset = ProjectMediaFormSet(
            request.POST,
            request.FILES,
            instance=project,
        )
        media_formset.require_media = False
        if form.is_valid() and media_formset.is_valid():
            project = _save_project_with_media(form, media_formset)
            messages.success(request, f'Project "{project.title or "Untitled"}" was updated successfully.')
            return redirect("home")
        return _render_home(
            request,
            form,
            media_formset,
            show_form=True,
            form_mode="edit",
            editing_project=project,
        )

    media_formset = ProjectMediaFormSet(instance=project)
    media_formset.require_media = False
    return _render_home(
        request,
        ProjectForm(instance=project),
        media_formset,
        show_form=True,
        form_mode="edit",
        editing_project=project,
    )


def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        title = project.title
        project.delete()
        messages.success(request, f'Project "{title}" was deleted successfully.')
    return redirect("home")


@xframe_options_sameorigin
def serve_project_game(request, pk, path=""):
    project = get_object_or_404(Project, pk=pk)
    if not project.is_web_game:
        raise Http404

    game_dir = Path(settings.GAMES_ROOT) / str(pk)
    if not game_dir.exists():
        raise Http404

    if not path:
        path = project.game_entry_point or "index.html"

    file_path = (game_dir / path).resolve()
    if not str(file_path).startswith(str(game_dir.resolve())):
        raise Http404
    if not file_path.is_file():
        raise Http404

    content_type, _ = mimetypes.guess_type(str(file_path))
    return FileResponse(
        open(file_path, "rb"),
        content_type=content_type or "application/octet-stream",
    )


class ProjectTypeViewSet(viewsets.ModelViewSet):
    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeSerializer
    permission_classes = []
    authentication_classes = []


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.prefetch_related("tags", "media").select_related("project_type")
    serializer_class = ProjectSerializer
    permission_classes = []
    authentication_classes = []


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = []
    authentication_classes = []


class ProjectMediaViewSet(viewsets.ModelViewSet):
    queryset = ProjectMedia.objects.all()
    serializer_class = ProjectMediaSerializer
    permission_classes = []
    authentication_classes = []
