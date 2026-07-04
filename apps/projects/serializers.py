import json

from rest_framework import serializers

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
from apps.projects.services.game_upload import process_project_game


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")


class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = "__all__"


class ProjectMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMedia
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.url:
            data["url"] = instance.url.url
        else:
            data["url"] = ""
        return data


def apply_project_tags(project, tag_names):
    tags = []
    for name in tag_names:
        name = str(name).strip()
        if name:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags.append(tag)
    project.tags.set(tags)


class TagListField(serializers.Field):
    def to_representation(self, value):
        if hasattr(value, "values_list"):
            return list(value.values_list("name", flat=True))
        if isinstance(value, list):
            return value
        return []

    def to_internal_value(self, data):
        if data is None:
            return []
        if isinstance(data, str):
            if not data.strip():
                return []
            try:
                parsed = json.loads(data)
                if isinstance(parsed, list):
                    return [str(item).strip() for item in parsed if str(item).strip()]
            except json.JSONDecodeError:
                pass
            return [item.strip() for item in data.split(",") if item.strip()]
        if isinstance(data, list):
            return [str(item).strip() for item in data if str(item).strip()]
        raise serializers.ValidationError("Tags must be a list of names.")


class ProjectSerializer(serializers.ModelSerializer):
    media = ProjectMediaSerializer(many=True, required=False)
    project_type_name = serializers.CharField(source="project_type.name", read_only=True)
    game_url = serializers.SerializerMethodField()
    tags = TagListField(required=False)

    class Meta:
        model = Project
        fields = (
            "id",
            "title",
            "role",
            "platform",
            "tech",
            "project_url",
            "github_url",
            "overview",
            "description",
            "display_mode",
            "game_zip",
            "game_entry_point",
            "project_type",
            "project_type_name",
            "game_url",
            "tags",
            "media",
        )
        extra_kwargs = {
            "title": {"required": False, "allow_blank": True},
            "overview": {"required": False, "allow_blank": True},
            "description": {"required": False, "allow_blank": True},
            "role": {"required": False, "allow_blank": True},
            "platform": {"required": False, "allow_blank": True},
            "tech": {"required": False},
            "project_url": {"required": False, "allow_blank": True},
            "github_url": {"required": False, "allow_blank": True},
            "project_type": {"required": False, "allow_null": True},
            "display_mode": {"required": False},
            "game_zip": {"required": False, "allow_null": True},
            "game_entry_point": {"required": False, "allow_blank": True},
        }

    def get_game_url(self, obj):
        return obj.game_url

    def validate_tech(self, value):
        if value is None:
            return []
        if isinstance(value, str):
            if not value.strip():
                return []
            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    return [str(item).strip() for item in parsed if str(item).strip()]
            except json.JSONDecodeError:
                pass
            return [item.strip() for item in value.split(",") if item.strip()]
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        return []

    def validate(self, attrs):
        project_type = attrs.get("project_type") or getattr(self.instance, "project_type", None)
        type_name = project_type.name if project_type else None

        if type_name not in ROLE_TYPES:
            attrs["role"] = ""
        if type_name not in URL_TYPES:
            attrs["project_url"] = ""
        if type_name not in GITHUB_TYPES:
            attrs["github_url"] = ""
        if type_name not in PLATFORM_TECH_TYPES:
            attrs["platform"] = ""
            attrs["tech"] = []

        if type_name != BUILDS:
            attrs["display_mode"] = DISPLAY_MODE_MEDIA
        else:
            display_mode = attrs.get(
                "display_mode",
                getattr(self.instance, "display_mode", DISPLAY_MODE_MEDIA),
            )
            if display_mode == DISPLAY_MODE_WEB_GAME:
                game_zip = attrs.get("game_zip")
                has_existing_zip = self.instance and self.instance.game_zip
                if not game_zip and not has_existing_zip:
                    raise serializers.ValidationError(
                        {"game_zip": "A zip file is required for playable web game projects."}
                    )

        return attrs

    def create(self, validated_data):
        media_data = validated_data.pop("media", [])
        tag_names = validated_data.pop("tags", [])
        project = Project.objects.create(**validated_data)
        apply_project_tags(project, tag_names)
        process_project_game(project)

        if not project.is_web_game:
            for media in media_data:
                if media.get("url"):
                    ProjectMedia.objects.create(project=project, **media)

        return project

    def update(self, instance, validated_data):
        media_data = validated_data.pop("media", None)
        tag_names = validated_data.pop("tags", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tag_names is not None:
            apply_project_tags(instance, tag_names)
        process_project_game(instance)

        if not instance.is_web_game and media_data is not None:
            instance.media.all().delete()
            for media in media_data:
                if media.get("url"):
                    ProjectMedia.objects.create(project=instance, **media)

        return instance
