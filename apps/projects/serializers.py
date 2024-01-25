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
    media = ProjectMediaSerializer(many=True)
    class Meta:
        model = Project
        fields = "__all__"