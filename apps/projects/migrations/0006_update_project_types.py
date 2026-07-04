from django.db import migrations

PROJECT_TYPES = [
    ("Software", "#7DE3A8"),
    ("Startups", "#EED17A"),
    ("Game Development", "#FC0303"),
    ("creative", "#DEB8F6"),
    ("Life", "#4FC3F7"),
]


def set_project_types(apps, schema_editor):
    ProjectType = apps.get_model("projects", "ProjectType")
    ProjectType.objects.all().delete()
    ProjectType.objects.bulk_create(
        [ProjectType(name=name, color=color) for name, color in PROJECT_TYPES]
    )


def unset_project_types(apps, schema_editor):
    ProjectType = apps.get_model("projects", "ProjectType")
    ProjectType.objects.all().delete()
    legacy_types = [
        ("Frontend", "#fc0303"),
        ("Backend", "#7DE3A8"),
        ("FullStack", "#EED17A"),
    ]
    ProjectType.objects.bulk_create(
        [ProjectType(name=name, color=color) for name, color in legacy_types]
    )


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0005_rename_media_projectmedia_url"),
    ]

    operations = [
        migrations.RunPython(set_project_types, unset_project_types),
    ]
