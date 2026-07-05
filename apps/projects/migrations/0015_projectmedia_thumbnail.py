from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0014_projectmedia_poster"),
    ]

    operations = [
        migrations.AddField(
            model_name="projectmedia",
            name="thumbnail",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
    ]
