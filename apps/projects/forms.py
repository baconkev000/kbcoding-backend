from django import forms
from django.forms import inlineformset_factory

from apps.projects.models import Project, ProjectMedia, ProjectType

INPUT_CLASS = "form-control"
TEXTAREA_CLASS = "form-control form-textarea"
SELECT_CLASS = "form-control form-select"
FILE_CLASS = "form-control form-file"


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("title", "project_type", "description", "overview")
        labels = {
            "title": "Project Name",
            "project_type": "Project Type",
            "description": "Project Description",
            "overview": "Project Overview",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT_CLASS, "id": "project-name"}),
            "project_type": forms.Select(attrs={"class": SELECT_CLASS}),
            "description": forms.Textarea(attrs={"class": TEXTAREA_CLASS, "rows": 3}),
            "overview": forms.Textarea(attrs={"class": TEXTAREA_CLASS, "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["project_type"].queryset = ProjectType.objects.all()
        for field in self.fields.values():
            field.required = True


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


class BaseProjectMediaFormSet(forms.BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return

        has_media = False
        for form in self.forms:
            if not form.cleaned_data or form.cleaned_data.get("DELETE"):
                continue
            name = form.cleaned_data.get("name")
            url = form.cleaned_data.get("url")
            if name or url:
                has_media = True
                if not name or not url:
                    raise forms.ValidationError(
                        "Each media item requires both a name and a file."
                    )

        if not has_media and getattr(self, "require_media", True):
            raise forms.ValidationError("Add at least one media file.")


ProjectMediaFormSet = inlineformset_factory(
    Project,
    ProjectMedia,
    form=ProjectMediaForm,
    formset=BaseProjectMediaFormSet,
    extra=1,
    can_delete=True,
)
