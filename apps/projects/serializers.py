import json

from rest_framework import serializers

from apps.projects.models import Project, ProjectMedia, ProjectType, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")


class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = "__all__"


class ProjectMediaSerializer(serializers.ModelSerializer):
    is_video = serializers.SerializerMethodField()

    class Meta:
        model = ProjectMedia
        fields = ("id", "name", "url", "poster", "thumbnail", "is_video")

    def get_is_video(self, obj):
        return obj.is_video

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.url:
            data["url"] = instance.url.url
        else:
            data["url"] = ""
        if instance.poster:
            data["poster"] = instance.poster.url
        else:
            data["poster"] = ""
        if instance.thumbnail:
            data["thumbnail"] = instance.thumbnail.url
        else:
            data["thumbnail"] = ""
        return data


class TagListField(serializers.Field):
    def to_representation(self, value):
        if hasattr(value, "values_list"):
            return list(value.values_list("name", flat=True))
        if isinstance(value, list):
            return value
        return []


class ProjectSerializer(serializers.ModelSerializer):
    media = ProjectMediaSerializer(many=True, read_only=True)
    project_type_name = serializers.CharField(source="project_type.name", read_only=True)
    project_type_color = serializers.CharField(source="project_type.color", read_only=True, allow_null=True)
    game_url = serializers.SerializerMethodField()
    tags = TagListField(read_only=True)

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
            "game_entry_point",
            "project_type",
            "project_type_name",
            "project_type_color",
            "game_url",
            "tags",
            "media",
        )
        read_only_fields = fields

    def get_game_url(self, obj):
        return obj.game_url

    def to_representation(self, instance):
        data = super().to_representation(instance)
        tech = data.get("tech")
        if isinstance(tech, str):
            if not tech.strip():
                data["tech"] = []
            else:
                try:
                    parsed = json.loads(tech)
                    data["tech"] = parsed if isinstance(parsed, list) else []
                except json.JSONDecodeError:
                    data["tech"] = [item.strip() for item in tech.split(",") if item.strip()]
        return data
