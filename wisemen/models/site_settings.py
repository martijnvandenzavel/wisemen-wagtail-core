from django.db.models import ForeignKey, SET_NULL
from django.utils.translation import gettext_lazy as _
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import MultiFieldPanel, FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.images import get_image_model_string


@register_setting(icon="placeholder")
class SiteSettings(ClusterableModel, BaseSiteSetting):
    """
    Site settings, collection of most commonly used settings.
    """
    logo = ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=SET_NULL,
        related_name="+",
        verbose_name=_("Logo"),
        help_text=_("Brand logo used in the navbar"),
    )

    seo_image = ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=SET_NULL,
        related_name="+",
        verbose_name=_("SEO Image"),
        help_text=_("Fallback image for social media sharing, can be overridden on each page"),
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("logo"),
            ],
            heading=_("Branding"),
        ),

        MultiFieldPanel(
            [
                FieldPanel("seo_image"),
            ],
            heading=_("SEO"),
        )
    ]