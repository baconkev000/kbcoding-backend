from django.contrib import admin
from apps.projects.models import Project, ProjectType, ProjectMedia

class ProjectAdmin(admin.ModelAdmin):
    pass


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectType, ProjectAdmin)
admin.site.register(ProjectMedia, ProjectAdmin)