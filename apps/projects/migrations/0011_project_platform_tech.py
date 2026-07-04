from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0010_optional_project_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="platform",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AddField(
            model_name="project",
            name="tech",
            field=models.JSONField(blank=True, default=list),
        ),
    ]
