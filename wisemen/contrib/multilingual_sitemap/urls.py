from django.urls import path
from django.views.decorators.cache import cache_page

from . import views as sitemaps_views
from .sitemap_generator import MultiLingualSitemap

app_name = "multilingual_sitemap"


class RoboJobSitemap(MultiLingualSitemap):
    priority = 0.5
    changefreq = "daily"
    protocol = "https"
    i18n = True
    alternates = True


sitemaps = {
    "sitemap": RoboJobSitemap,
}

urlpatterns = [
    path(
        "sitemap.xml",
        cache_page(14400)(sitemaps_views.sitemap),  # Cache for 4 hours.
        {"sitemaps": sitemaps},
        name="multilingual_sitemap.views.sitemap",
    ),
]
