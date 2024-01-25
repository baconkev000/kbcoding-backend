from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from apps.projects.views import ProjectTypeViewSet, ProjectViewSet, ProjectMediaViewSet

from backend.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register(r'project_types', ProjectTypeViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'project_media', ProjectMediaViewSet)



app_name = "api"
urlpatterns = router.urls
