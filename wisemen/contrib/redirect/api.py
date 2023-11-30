from django.conf import settings
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from wagtail.contrib.redirects.models import Redirect
from wagtail.models import Locale


@extend_schema(tags=["Redirects"])
@parser_classes((JSONParser,))
class RedirectAPIView(generics.GenericAPIView):
    """
    API endpoint that returns an external or internal link
    to redirect to if the original link is known.
    """

    def redirect_page_convert(self, obj):
        """
        Convert the given URL or Wagtail page into a proper path.
        """
        if obj.redirect_link:
            return [True, obj.redirect_link]

        if obj.redirect_page:
            page_locale: Locale = obj.redirect_page.locale
            homepage_model = settings.WISEMEN_HOMEPAGE_MODEL
            homepage = homepage_model.objects.filter(locale=page_locale).first()

            return [
                False,
                f"/{page_locale.language_code}{obj.redirect_page.url_path.removeprefix('/' + homepage.slug)}",
            ]

    def post(self, request, *args, **kwargs):
        try:
            url = request.data["url"]
        except:
            return Response({"hasRedirect": False})

        redirect = Redirect.objects.filter(old_path=url).first()

        if redirect:
            external, to = self.redirect_page_convert(redirect)

            return Response(
                {
                    "from": redirect.old_path,
                    "to": to,
                    "external": external,
                    "statusCode": 301 if redirect.is_permanent else 302,
                }
            )
        else:
            return Response({"hasRedirect": False})
