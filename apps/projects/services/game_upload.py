import shutil
import zipfile
from pathlib import Path

from django.conf import settings

from apps.projects.constants import DISPLAY_MODE_MEDIA


def get_game_dir(project_id: int) -> Path:
    return Path(settings.GAMES_ROOT) / str(project_id)


def cleanup_game_dir(project_id: int) -> None:
    game_dir = get_game_dir(project_id)
    if game_dir.exists():
        shutil.rmtree(game_dir)


def find_entry_point(root: Path, filename: str = "index.html") -> str:
    if (root / filename).exists():
        return filename

    for child in sorted(root.iterdir()):
        if child.is_dir() and (child / filename).exists():
            return str(Path(child.name) / filename).replace("\\", "/")

    for path in sorted(root.rglob(filename)):
        return str(path.relative_to(root)).replace("\\", "/")

    return filename


def extract_game_zip(project) -> None:
    if not project.game_zip:
        raise ValueError("No game zip file uploaded.")

    cleanup_game_dir(project.pk)
    game_dir = get_game_dir(project.pk)
    game_dir.mkdir(parents=True, exist_ok=True)

    zip_path = Path(project.game_zip.path)
    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.namelist():
            if member.endswith("/"):
                continue
            target = (game_dir / member).resolve()
            if not str(target).startswith(str(game_dir.resolve())):
                raise ValueError("Unsafe path in zip archive.")
        archive.extractall(game_dir)

    entry_point = find_entry_point(game_dir)
    project.game_entry_point = entry_point
    project.save(update_fields=["game_entry_point"])


def process_project_game(project, *, previous_display_mode: str | None = None) -> None:
    if project.display_mode == DISPLAY_MODE_MEDIA:
        cleanup_game_dir(project.pk)
        if project.game_zip:
            project.game_zip.delete(save=False)
            project.game_zip = None
            project.game_entry_point = "index.html"
            project.save(update_fields=["game_zip", "game_entry_point"])
        return

    if project.game_zip:
        extract_game_zip(project)


def cleanup_project_game(project) -> None:
    cleanup_game_dir(project.pk)
    if project.game_zip:
        project.game_zip.delete(save=False)
