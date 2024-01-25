from django.db import models

class ProjectType(models.Model):
    """
    Project Type
    A class model for a Project Type
    """

    name = models.CharField(max_length=255, null=False)
    color = models.CharField(max_length=255, null=False)

    class Meta:
        verbose_name_plural = "Project Types"

    def __str__(self):
        return self.name

class Project(models.Model):
    """
    Project
    A class model for a Project
    """

    title = models.CharField(max_length=255, null=False)
    overview = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, null=False)
    project_type = models.ForeignKey(ProjectType, null=True, on_delete=models.SET_NULL, related_name="project")


    class Meta:
        verbose_name_plural = "Projects"

    def __str__(self):
        return f"{self.title}"
    
class ProjectMedia(models.Model):
    """
    Project Media
    A class model for Project Media
    """
    name = models.CharField(max_length=255, null=False)
    url = models.FileField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="media")

    class Meta:
        verbose_name_plural = "Project Media"

    def __str__(self):
        return f"{self.name} - {self.project}"
    

