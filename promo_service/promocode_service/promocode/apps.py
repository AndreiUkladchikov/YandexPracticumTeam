from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PromocodeConfig(AppConfig):

    default_auto_field = "django.db.models.AutoField"
    name = "promocode"
    verbose_name = _("promocodes")

    def ready(self):
        """Loading promocode models signals when app is ready."""
        import promocode.signals
