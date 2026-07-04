from django.db import models

from apps.projects.constants import DISPLAY_MODE_MEDIA, DISPLAY_MODE_WEB_GAME


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

    title = models.CharField(max_length=255, blank=True, default="")
    role = models.CharField(max_length=255, blank=True, default="")
    platform = models.CharField(max_length=255, blank=True, default="")
    tech = models.JSONField(blank=True, default=list)
    project_url = models.URLField(max_length=500, blank=True, default="")
    github_url = models.URLField(max_length=500, blank=True, default="")
    overview = models.TextField(blank=True, default="")
    description = models.TextField(blank=True, default="")
    display_mode = models.CharField(
        max_length=20,
        choices=[
            (DISPLAY_MODE_MEDIA, "Media-only project"),
            (DISPLAY_MODE_WEB_GAME, "Playable web game"),
        ],
        default=DISPLAY_MODE_MEDIA,
    )
    game_zip = models.FileField(upload_to="game_zips/", blank=True, null=True)
    game_entry_point = models.CharField(max_length=255, blank=True, default="index.html")
    project_type = models.ForeignKey(ProjectType, null=True, on_delete=models.SET_NULL, related_name="project")
    tags = models.ManyToManyField("Tag", blank=True, related_name="projects")

    @property
    def is_web_game(self):
        return self.display_mode == DISPLAY_MODE_WEB_GAME

    @property
    def game_url(self):
        if not self.is_web_game or not self.pk:
            return ""
        entry = self.game_entry_point or "index.html"
        return f"/projects/{self.pk}/game/{entry}"


    class Meta:
        verbose_name_plural = "Projects"

    def __str__(self):
        return f"{self.title}"

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class ProjectMedia(models.Model):
    """
    Project Media
    A class model for Project Media
    """
    name = models.CharField(max_length=255, blank=True, default="")
    url = models.FileField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="media")

    class Meta:
        verbose_name_plural = "Project Media"

    def __str__(self):
        return f"{self.name} - {self.project}"

    @property
    def is_video(self):
        if not self.url:
            return False
        video_extensions = (".mp4", ".webm", ".mov", ".avi", ".mkv", ".ogg")
        return self.url.name.lower().endswith(video_extensions)

