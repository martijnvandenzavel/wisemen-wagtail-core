from django.contrib.sitemaps import Sitemap as DjangoSitemap
from django.conf import settings


class MultiLingualSitemap(DjangoSitemap):
    """
    Slightly altered implementation of Wagtail's Sitemap generator
    to implement multilingual sitemap URLs.
    """

    def __init__(self, request=None):
        self.request = request

    def _urls(self, page, protocol, domain):
        """
        Override to not include pages which return
        an empty list on their get_sitemap_urls() method
        and thus want to be excluded.

        :param page:
        :param protocol:
        :param domain:
        :return:
        """
        urls = []
        latest_lastmod = None
        all_items_lastmod = True  # track if all items have a lastmod

        paginator_page = self.paginator.page(page)
        for item in paginator_page.object_list:
            # Nothing (empty list) returns from get_sitemap_urls?
            # Skip it as it wants to be excluded.
            if not item[0].get_sitemap_urls():
                continue

            loc = f"{protocol}://{domain}{self._location(item)}"
            priority = self._get("priority", item)
            lastmod = self._get("lastmod", item)

            if all_items_lastmod:
                all_items_lastmod = lastmod is not None
                if all_items_lastmod and (
                    latest_lastmod is None or lastmod > latest_lastmod
                ):
                    latest_lastmod = lastmod

            url_info = {
                "item": item,
                "location": loc,
                "lastmod": lastmod,
                "changefreq": self._get("changefreq", item),
                "priority": str(priority if priority is not None else ""),
                "alternates": [],
            }

            if self.i18n and self.alternates:
                for lang_code in self._languages():
                    loc = f"{protocol}://{domain}{self._location(item, lang_code)}"
                    url_info["alternates"].append(
                        {
                            "location": loc,
                            "lang_code": lang_code,
                        }
                    )
                if self.x_default:
                    lang_code = settings.LANGUAGE_CODE
                    loc = f"{protocol}://{domain}{self._location(item, lang_code)}"
                    loc = loc.replace(f"/{lang_code}/", "/", 1)
                    url_info["alternates"].append(
                        {
                            "location": loc,
                            "lang_code": "x-default",
                        }
                    )

            urls.append(url_info)

        if all_items_lastmod and latest_lastmod:
            self.latest_lastmod = latest_lastmod

        return urls

    def location(self, obj):
        """
        Return the localized URL prefixed by the language code
        to mimic the front-end URL behavior.
        """
        return f"/{obj.localized.locale.language_code}{obj.localized.get_url(self.request)}"

    def lastmod(self, obj):
        # fall back on latest_revision_created_at if last_published_at is null
        # (for backwards compatibility from before last_published_at was added)
        return obj.last_published_at or obj.latest_revision_created_at

    def get_wagtail_site(self):
        from wagtail.models import Site

        site = Site.find_for_request(self.request)
        if site is None:
            return Site.objects.select_related("root_page").get(is_default_site=True)
        return site

    def items(self):
        return (
            self.get_wagtail_site()
            .root_page.get_descendants(inclusive=True)
            .live()
            .public()
            .order_by("path")
            .defer_streamfields()
            .specific()
        )
