from django.urls import path
from gdg_be.core.api.views import (
    ResourceViewSet,
    ProjectViewSet,
    StepViewSet,
    UserProjectViewSet,
    NewProjectView,
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"resources", ResourceViewSet)
router.register(r"projects", ProjectViewSet)
router.register(r"steps", StepViewSet)
router.register(r"user-projects", UserProjectViewSet)

urlpatterns = router.urls + [path("new-project", NewProjectView.as_view())]
