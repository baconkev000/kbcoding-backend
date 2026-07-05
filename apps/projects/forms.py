import json

from django import forms
from django.conf import settings
from django.forms import inlineformset_factory

from apps.projects.constants import (
    BUILDS,
    DISPLAY_MODE_MEDIA,
    DISPLAY_MODE_WEB_GAME,
    GITHUB_TYPES,
    PLATFORM_TECH_TYPES,
    ROLE_TYPES,
    URL_TYPES,
)
from apps.projects.models import Project, ProjectMedia, ProjectType, Tag

INPUT_CLASS = "form-control"
TEXTAREA_CLASS = "form-control form-textarea"
SELECT_CLASS = "form-control form-select"
FILE_CLASS = "form-control form-file"
URL_CLASS = "form-control"


class ProjectForm(forms.ModelForm):
    tag_names = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={"id": "id_tag_names"}),
    )

    class Meta:
        model = Project
        fields = (
            "title",
            "project_type",
            "role",
            "platform",
            "tech",
            "project_url",
            "github_url",
            "description",
            "overview",
            "display_mode",
            "game_zip",
        )
        labels = {
            "title": "Project Name",
            "project_type": "Project Type",
            "role": "Role",
            "platform": "Platform",
            "tech": "Tech",
            "project_url": "URL",
            "github_url": "GitHub URL",
            "description": "Project Description",
            "overview": "Project Overview",
            "display_mode": "Project Display",
            "game_zip": "Playable Web Game (ZIP)",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT_CLASS, "id": "project-name"}),
            "project_type": forms.Select(attrs={"class": SELECT_CLASS, "id": "id_project_type"}),
            "role": forms.TextInput(attrs={"class": INPUT_CLASS, "id": "id_role"}),
            "platform": forms.TextInput(attrs={"class": INPUT_CLASS, "id": "id_platform"}),
            "tech": forms.HiddenInput(attrs={"id": "id_tech"}),
            "project_url": forms.URLInput(attrs={"class": URL_CLASS, "id": "id_project_url", "placeholder": "https://"}),
            "github_url": forms.URLInput(attrs={"class": URL_CLASS, "id": "id_github_url", "placeholder": "https://github.com/..."}),
            "description": forms.Textarea(attrs={"class": TEXTAREA_CLASS, "rows": 6}),
            "overview": forms.Textarea(attrs={"class": TEXTAREA_CLASS, "rows": 6}),
            "display_mode": forms.RadioSelect(
                choices=[
                    (DISPLAY_MODE_MEDIA, "Media-only project"),
                    (DISPLAY_MODE_WEB_GAME, "Playable web game (upload zip)"),
                ],
                attrs={"class": "display-mode-radio"},
            ),
            "game_zip": forms.ClearableFileInput(
                attrs={
                    "class": FILE_CLASS,
                    "id": "id_game_zip",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["project_type"].queryset = ProjectType.objects.all()
        self.fields["project_type"].required = False
        self.fields["project_type"].empty_label = "Select a type (optional)"
        for field in self.fields.values():
            field.required = False
        if self.instance.pk:
            self.fields["tag_names"].initial = json.dumps(
                list(self.instance.tags.values_list("name", flat=True))
            )

    def clean_game_zip(self):
        game_zip = self.cleaned_data.get("game_zip")
        if not game_zip:
            return game_zip

        if hasattr(game_zip, "size") and game_zip.size > settings.MAX_GAME_ZIP_SIZE:
            raise forms.ValidationError("Zip file is too large.")

        if hasattr(game_zip, "name") and not game_zip.name.lower().endswith(".zip"):
            raise forms.ValidationError("Please upload a .zip file.")

        return game_zip

    def clean(self):
        cleaned_data = super().clean()
        project_type = cleaned_data.get("project_type")
        type_name = project_type.name if project_type else None

        if type_name not in ROLE_TYPES:
            cleaned_data["role"] = ""
        if type_name not in URL_TYPES:
            cleaned_data["project_url"] = ""
        if type_name not in GITHUB_TYPES:
            cleaned_data["github_url"] = ""
        if type_name not in PLATFORM_TECH_TYPES:
            cleaned_data["platform"] = ""
            cleaned_data["tech"] = []

        if type_name != BUILDS:
            cleaned_data["display_mode"] = DISPLAY_MODE_MEDIA
        elif cleaned_data.get("display_mode") == DISPLAY_MODE_WEB_GAME:
            game_zip = cleaned_data.get("game_zip")
            has_existing = self.instance.pk and self.instance.game_zip
            if not game_zip and not has_existing:
                self.add_error("game_zip", "Upload a zip file containing your web game export.")

        return cleaned_data

    def save(self, commit=True):
        project = super().save(commit=commit)
        if commit:
            self._save_tags(project)
        return project

    def _save_tags(self, project):
        raw = self.cleaned_data.get("tag_names") or "[]"
        try:
            names = json.loads(raw)
        except json.JSONDecodeError:
            names = []
        tags = []
        for name in names:
            name = str(name).strip()
            if name:
                tag, _ = Tag.objects.get_or_create(name=name)
                tags.append(tag)
        project.tags.set(tags)


class ProjectMediaForm(forms.ModelForm):
    class Meta:
        model = ProjectMedia
        fields = ("name", "url")
        labels = {
            "name": "Media Name",
            "url": "Media File",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "url": forms.ClearableFileInput(
                attrs={
                    "class": FILE_CLASS,
                    "accept": "image/*,video/*",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = False
        self.fields["url"].required = False


class BaseProjectMediaFormSet(forms.BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return

        for form in self.forms:
            if not form.cleaned_data or form.cleaned_data.get("DELETE"):
                continue
            name = form.cleaned_data.get("name", "")
            url = form.cleaned_data.get("url")
            if not url and not str(name).strip():
                form.cleaned_data["DELETE"] = True


ProjectMediaFormSet = inlineformset_factory(
    Project,
    ProjectMedia,
    form=ProjectMediaForm,
    formset=BaseProjectMediaFormSet,
    extra=0,
    can_delete=True,
)
