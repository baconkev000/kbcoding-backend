from rest_framework import serializers
from apps.projects.models import ProjectType,Project,ProjectMedia

class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = "__all__"

class ProjectMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMedia
        fields = "__all__"

class ProjectSerializer(serializers.ModelSerializer):
    media = ProjectMediaSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = "__all__"

    def create(self, validated_data):
        media_data = validated_data.pop('media', [])  # Extract media if provided
        project = Project.objects.create(**validated_data)  # Create the project instance

        # Create associated media objects
        for media in media_data:
            ProjectMedia.objects.create(project=project, **media)

        return project
