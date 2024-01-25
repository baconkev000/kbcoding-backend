from django.shortcuts import render
from rest_framework import status, viewsets
from apps.projects.models import ProjectType,Project,ProjectMedia
from apps.projects.serializers import ProjectMediaSerializer,ProjectSerializer,ProjectTypeSerializer

class ProjectTypeViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing projects.
    """
    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeSerializer
    permission_classes = []
    authentication_classes = []

class ProjectViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing projects.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = []
    authentication_classes = []

class ProjectMediaViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing projects.
    """
    queryset = ProjectMedia.objects.all()
    serializer_class = ProjectMediaSerializer
    permission_classes = []
    authentication_classes = []