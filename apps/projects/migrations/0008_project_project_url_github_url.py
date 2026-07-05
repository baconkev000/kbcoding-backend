from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0007_project_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="project_url",
            field=models.URLField(blank=True, default="", max_length=500),
        ),
        migrations.AddField(
            model_name="project",
            name="github_url",
            field=models.URLField(blank=True, default="", max_length=500),
        ),
    ]
