import inspect

from django.contrib.sitemaps import views as sitemap_views


def index(request, sitemaps, **kwargs):
    sitemaps = prepare_sitemaps(request, sitemaps)

    response = sitemap_views.index(request, sitemaps, **kwargs)

    return response


def sitemap(request, sitemaps=None, **kwargs):
    from .sitemap_generator import MultiLingualSitemap

    if sitemaps:
        sitemaps = prepare_sitemaps(request, sitemaps)
    else:
        sitemaps = {"wagtail": MultiLingualSitemap(request)}

    response = sitemap_views.sitemap(
        request, sitemaps, template_name="sitemap_alternates.xml", **kwargs
    )

    return response


def prepare_sitemaps(request, sitemaps):
    from .sitemap_generator import MultiLingualSitemap

    initialised_sitemaps = {}
    for name, sitemap_cls in sitemaps.items():
        if inspect.isclass(sitemap_cls) and issubclass(
            sitemap_cls, MultiLingualSitemap
        ):
            initialised_sitemaps[name] = sitemap_cls(request)
        else:
            initialised_sitemaps[name] = sitemap_cls
    return initialised_sitemaps
