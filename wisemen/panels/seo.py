from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.admin.widgets.slug import SlugInput


def seo_panels(disable_slug=False):
    # Grays out the slug field in the admin panel, so it can't be edited.
    widget = SlugInput(attrs={"style": "pointer-events: none;background-color:#E9ECEF"})

    if disable_slug:
        return [
            MultiFieldPanel(
                [
                    FieldPanel("slug", widget=widget),
                    FieldPanel("seo_title"),
                    FieldPanel("search_description"),
                    FieldPanel("og_image"),
                ],
                _("Search and Social Previews"),
            )
        ]
    else:
        return [
            MultiFieldPanel(
                [
                    FieldPanel("slug", widget=SlugInput),
                    FieldPanel("seo_title"),
                    FieldPanel("search_description"),
                    FieldPanel("og_image"),
                ],
                _("Search and Social Previews"),
            )
        ]
