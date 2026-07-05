import logging
import shutil
import subprocess
import tempfile
from pathlib import Path

from django.core.files import File

logger = logging.getLogger(__name__)

VIDEO_EXTENSIONS = (".mp4", ".webm", ".mov", ".avi", ".mkv", ".ogg")
PROCESSED_VIDEO_SUFFIX = "_web.mp4"
POSTER_SUFFIX = "_poster.jpg"
THUMBNAIL_SUFFIX = "_thumb.jpg"

MAX_VIDEO_WIDTH = 1280
POSTER_WIDTH = 960
THUMBNAIL_WIDTH = 320


def is_video_filename(name: str) -> bool:
    return name.lower().endswith(VIDEO_EXTENSIONS)


def is_processed_video(name: str) -> bool:
    return name.lower().endswith(PROCESSED_VIDEO_SUFFIX)


def _run_ffmpeg(args: list[str]) -> None:
    result = subprocess.run(
        ["ffmpeg", *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffmpeg failed")


def _extract_frame(source: Path, output: Path, width: int, quality: int) -> None:
    for seek in ("00:00:00.5", "00:00:00"):
        try:
            _run_ffmpeg(
                [
                    "-y",
                    "-ss",
                    seek,
                    "-i",
                    str(source),
                    "-vframes",
                    "1",
                    "-vf",
                    f"scale='min({width},iw)':-2",
                    "-q:v",
                    str(quality),
                    str(output),
                ]
            )
            if output.exists() and output.stat().st_size > 0:
                return
        except RuntimeError:
            continue
    raise RuntimeError(f"Could not extract frame from {source}")


def process_project_media_video(media, *, force: bool = False) -> bool:
    """Transcode video for fast web playback and generate poster/thumbnail images."""
    if not media.url:
        return False
    if not is_video_filename(media.url.name):
        return False
    if (
        not force
        and is_processed_video(media.url.name)
        and media.poster
        and media.thumbnail
    ):
        return False
    if not shutil.which("ffmpeg"):
        logger.warning("ffmpeg not installed; skipping video optimization for media %s", media.pk)
        return False

    source = Path(media.url.path)
    if not source.exists():
        logger.warning("Video file missing for media %s: %s", media.pk, source)
        return False

    old_url_name = media.url.name
    old_poster_name = media.poster.name if media.poster else None
    old_thumbnail_name = media.thumbnail.name if media.thumbnail else None
    stem = Path(source.name).stem
    if stem.endswith("_web"):
        stem = stem[:-4]

    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            optimized = tmp_dir / "optimized.mp4"
            poster = tmp_dir / "poster.jpg"
            thumbnail = tmp_dir / "thumb.jpg"

            _run_ffmpeg(
                [
                    "-y",
                    "-i",
                    str(source),
                    "-vf",
                    f"scale='min({MAX_VIDEO_WIDTH},iw)':-2",
                    "-c:v",
                    "libx264",
                    "-crf",
                    "28",
                    "-preset",
                    "fast",
                    "-c:a",
                    "aac",
                    "-b:a",
                    "96k",
                    "-movflags",
                    "+faststart",
                    "-pix_fmt",
                    "yuv420p",
                    str(optimized),
                ]
            )
            _extract_frame(optimized, poster, POSTER_WIDTH, 3)
            _extract_frame(optimized, thumbnail, THUMBNAIL_WIDTH, 6)

            with optimized.open("rb") as video_file:
                media.url.save(f"{stem}{PROCESSED_VIDEO_SUFFIX}", File(video_file), save=False)
            with poster.open("rb") as poster_file:
                media.poster.save(f"{stem}{POSTER_SUFFIX}", File(poster_file), save=False)
            with thumbnail.open("rb") as thumb_file:
                media.thumbnail.save(f"{stem}{THUMBNAIL_SUFFIX}", File(thumb_file), save=False)

        media._skip_video_processing = True
        media.save(update_fields=["url", "poster", "thumbnail"])

        if old_url_name and old_url_name != media.url.name:
            media.url.storage.delete(old_url_name)
        if old_poster_name and old_poster_name != media.poster.name:
            media.poster.storage.delete(old_poster_name)
        if old_thumbnail_name and old_thumbnail_name != media.thumbnail.name:
            media.thumbnail.storage.delete(old_thumbnail_name)

        logger.info("Optimized video for media %s", media.pk)
        return True
    except Exception:
        logger.exception("Failed to optimize video for media %s", media.pk)
        return False
