from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0006_update_project_types"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="role",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
    ]
