from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import viewsets

from apps.projects.forms import ProjectForm, ProjectMediaFormSet
from apps.projects.models import Project, ProjectMedia, ProjectType
from apps.projects.serializers import (
    ProjectMediaSerializer,
    ProjectSerializer,
    ProjectTypeSerializer,
)


def _render_home(request, form, media_formset, *, show_form=False, form_mode="add", editing_project=None):
    return render(
        request,
        "pages/home.html",
        {
            "form": form,
            "media_formset": media_formset,
            "projects": Project.objects.select_related("project_type").order_by("title"),
            "show_form": show_form,
            "form_mode": form_mode,
            "editing_project": editing_project,
        },
    )


def home(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        media_formset = ProjectMediaFormSet(request.POST, request.FILES)
        if form.is_valid() and media_formset.is_valid():
            project = form.save()
            media_formset.instance = project
            media_formset.save()
            messages.success(request, f'Project "{project.title}" was created successfully.')
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
        form = ProjectForm(request.POST, instance=project)
        media_formset = ProjectMediaFormSet(
            request.POST,
            request.FILES,
            instance=project,
        )
        media_formset.require_media = False
        if form.is_valid() and media_formset.is_valid():
            form.save()
            media_formset.save()
            messages.success(request, f'Project "{project.title}" was updated successfully.')
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


class ProjectTypeViewSet(viewsets.ModelViewSet):
    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeSerializer
    permission_classes = []
    authentication_classes = []


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = []
    authentication_classes = []


class ProjectMediaViewSet(viewsets.ModelViewSet):
    queryset = ProjectMedia.objects.all()
    serializer_class = ProjectMediaSerializer
    permission_classes = []
    authentication_classes = []
