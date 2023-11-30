from datetime import datetime
from django.conf import settings
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import BlacklistMixin
from django.utils.translation import gettext_lazy as _


class BlacklistWithGracePeriodMixin(BlacklistMixin):
    """
    Extension on the BlackListMixin which takes into account the
    grace periode of a refresh token if configured.
    """

    if "rest_framework_simplejwt.token_blacklist" in settings.INSTALLED_APPS:

        def verify(self, *args, **kwargs):
            self.check_blacklist()

            super().verify(*args, **kwargs)

        def check_blacklist(self):
            """
            Checks if this token is present in the token blacklist.
            If there is no grace period set, raise `TokenError` if so.
            Else check if we are within the grace period, otherwise raise the error either way.
            """
            jti = self.payload[api_settings.JTI_CLAIM]
            grace_period = None
            if "REFRESH_TOKEN_GRACE_PERIOD" in settings.SIMPLE_JWT:
                grace_period = settings.SIMPLE_JWT["REFRESH_TOKEN_GRACE_PERIOD"]

            try:
                blacklisted_token = BlacklistedToken.objects.filter(token__jti=jti).get()

                if blacklisted_token:
                    if not grace_period:
                        raise TokenError(_("Token is blacklisted"))
                    else:
                        # If the current time is larger than the blacklisted time + its grace period, its invalid.
                        if datetime.utcnow() > (blacklisted_token.blacklisted_at.replace(tzinfo=None) + grace_period):
                            raise TokenError(_("Token is blacklisted"))
            except BlacklistedToken.DoesNotExist:
                pass
