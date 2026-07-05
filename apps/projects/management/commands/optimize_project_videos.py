from django.core.management.base import BaseCommand

from apps.projects.models import ProjectMedia
from apps.projects.services.video_upload import process_project_media_video


class Command(BaseCommand):
    help = "Optimize existing project videos for web playback and generate poster/thumbnail images."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Reprocess videos even if poster/thumbnail already exist.",
        )

    def handle(self, *args, **options):
        force = options["force"]
        media_items = ProjectMedia.objects.exclude(url="").order_by("id")
        processed = 0
        skipped = 0
        failed = 0

        for media in media_items:
            if not media.is_video:
                skipped += 1
                continue
            if media.poster and media.thumbnail and not force:
                skipped += 1
                continue

            if force:
                if media.poster:
                    media.poster.delete(save=False)
                    media.poster = None
                if media.thumbnail:
                    media.thumbnail.delete(save=False)
                    media.thumbnail = None
                media._skip_video_processing = True
                media.save(update_fields=["poster", "thumbnail"])

            if process_project_media_video(media, force=force):
                processed += 1
                self.stdout.write(self.style.SUCCESS(f"Optimized media {media.pk}: {media.name}"))
            else:
                failed += 1
                self.stdout.write(self.style.WARNING(f"Skipped media {media.pk}: {media.name}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. processed={processed} skipped={skipped} failed={failed}"
            )
        )
