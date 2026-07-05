from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0011_project_platform_tech"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="display_mode",
            field=models.CharField(
                choices=[
                    ("media", "Media-only project"),
                    ("web_game", "Playable web game"),
                ],
                default="media",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="game_entry_point",
            field=models.CharField(blank=True, default="index.html", max_length=255),
        ),
        migrations.AddField(
            model_name="project",
            name="game_zip",
            field=models.FileField(blank=True, null=True, upload_to="game_zips/"),
        ),
    ]
