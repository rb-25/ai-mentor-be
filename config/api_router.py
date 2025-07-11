from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter
from django.urls import path, include

from gdg_be.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns = [
    path("users/", include("gdg_be.users.api.urls")),
    path("core/", include("gdg_be.core.api.urls")),
]
urlpatterns += router.urls
