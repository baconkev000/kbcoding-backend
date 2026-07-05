from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0009_alter_project_description_overview"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="title",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AlterField(
            model_name="project",
            name="overview",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="project",
            name="description",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="projectmedia",
            name="name",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AlterField(
            model_name="projectmedia",
            name="url",
            field=models.FileField(blank=True, null=True, upload_to=""),
        ),
    ]
