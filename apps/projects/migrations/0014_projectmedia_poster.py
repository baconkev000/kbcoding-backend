from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0013_tag_and_project_types"),
    ]

    operations = [
        migrations.AddField(
            model_name="projectmedia",
            name="poster",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
    ]
