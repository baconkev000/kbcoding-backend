from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0008_project_project_url_github_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="description",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="project",
            name="overview",
            field=models.TextField(),
        ),
    ]
