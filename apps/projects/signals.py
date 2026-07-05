from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from apps.projects.models import Project, ProjectMedia
from apps.projects.services.game_upload import cleanup_project_game
from apps.projects.services.video_upload import process_project_media_video


@receiver(post_delete, sender=Project)
def delete_project_game_files(sender, instance, **kwargs):
    cleanup_project_game(instance)


@receiver(pre_save, sender=ProjectMedia)
def track_project_media_url_change(sender, instance, **kwargs):
    if instance.pk:
        try:
            previous = ProjectMedia.objects.get(pk=instance.pk)
            instance._url_changed = previous.url != instance.url
        except ProjectMedia.DoesNotExist:
            instance._url_changed = bool(instance.url)
    else:
        instance._url_changed = bool(instance.url)


@receiver(post_save, sender=ProjectMedia)
def optimize_project_media_video(sender, instance, **kwargs):
    if getattr(instance, "_skip_video_processing", False):
        return
    if not instance.url:
        return
    if not getattr(instance, "_url_changed", True) and instance.poster:
        return
    process_project_media_video(instance)
