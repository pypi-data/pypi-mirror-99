from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class NotificationsConfig(AppConfig):
    name = "vng_api_common.notifications"
    verbose_name = _("Notificaties")
