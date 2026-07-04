from django.db import migrations, models


SEED_TAGS = [
    "Startup",
    "SaaS",
    "Game",
    "Prototype",
    "Digital art",
    "UI design experiments",
    "Visual work",
]

NEW_TYPES = [
    ("Builds", "#EED17A"),
    ("Creative", "#DEB8F6"),
    ("Life / Other", "#4FC3F7"),
]

OLD_TYPE_MAP = {
    "Software": ("Builds", "SaaS"),
    "Startups": ("Builds", "Startup"),
    "Game Development": ("Builds", "Game"),
    "creative": ("Creative", None),
    "Life": ("Life / Other", None),
}


def migrate_project_types_and_tags(apps, schema_editor):
    ProjectType = apps.get_model("projects", "ProjectType")
    Project = apps.get_model("projects", "Project")
    Tag = apps.get_model("projects", "Tag")

    tag_by_name = {}
    for name in SEED_TAGS:
        tag_by_name[name] = Tag.objects.create(name=name)

    old_types = list(ProjectType.objects.all())
    old_id_map = {}
    for old_type in old_types:
        if old_type.name in OLD_TYPE_MAP:
            old_id_map[old_type.id] = OLD_TYPE_MAP[old_type.name]

    ProjectType.objects.all().delete()
    new_types_by_name = {}
    for name, color in NEW_TYPES:
        new_types_by_name[name] = ProjectType.objects.create(name=name, color=color)

    for project in Project.objects.all():
        mapping = old_id_map.get(project.project_type_id)
        if not mapping:
            continue
        new_name, tag_name = mapping
        project.project_type = new_types_by_name[new_name]
        project.save(update_fields=["project_type"])
        if tag_name and tag_name in tag_by_name:
            project.tags.add(tag_by_name[tag_name])


def reverse_migration(apps, schema_editor):
    ProjectType = apps.get_model("projects", "ProjectType")
    Tag = apps.get_model("projects", "Tag")

    Tag.objects.all().delete()
    ProjectType.objects.all().delete()
    legacy_types = [
        ("Software", "#7DE3A8"),
        ("Startups", "#EED17A"),
        ("Game Development", "#FC0303"),
        ("creative", "#DEB8F6"),
        ("Life", "#4FC3F7"),
    ]
    ProjectType.objects.bulk_create(
        [ProjectType(name=name, color=color) for name, color in legacy_types]
    )


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0012_project_web_game"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.AddField(
            model_name="project",
            name="tags",
            field=models.ManyToManyField(blank=True, related_name="projects", to="projects.tag"),
        ),
        migrations.RunPython(migrate_project_types_and_tags, reverse_migration),
    ]
