from django.urls import path

from .views import UpdateUser

urlpatterns = [
    path("update/", UpdateUser.as_view(), name="update-user"),
]
