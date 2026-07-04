from django.db.models.signals import post_delete
from django.dispatch import receiver

from apps.projects.models import Project
from apps.projects.services.game_upload import cleanup_project_game


@receiver(post_delete, sender=Project)
def delete_project_game_files(sender, instance, **kwargs):
    cleanup_project_game(instance)
