import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from config.settings.firebase_config import initialize_firebase_admin


class UsersConfig(AppConfig):
    name = "gdg_be.users"
    verbose_name = _("Users")

    def ready(self):
        with contextlib.suppress(ImportError):
            import gdg_be.users.signals  # noqa: F401, PLC0415

        initialize_firebase_admin()
