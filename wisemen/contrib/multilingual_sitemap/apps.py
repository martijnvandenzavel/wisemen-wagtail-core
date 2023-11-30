from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MultilingualSitemapAppConfig(AppConfig):
    name = "wisemen.contrib.multilingual_sitemap"
    label = "multilingual_sitemap"
    verbose_name = _("Multilingual sitemap")
