from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import Token, AccessToken

from rest_framework_simplejwt_with_grace_period.mixins.blacklist import BlacklistWithGracePeriodMixin


class RefreshWithGracePeriodToken(BlacklistWithGracePeriodMixin, Token):
    """
    Reproduction of the original RefreshToken from rest_framework_simplejwt.
    Needed to mixin our own BlacklistMixin.
    """
    token_type = "refresh"
    lifetime = api_settings.REFRESH_TOKEN_LIFETIME
    no_copy_claims = (
        api_settings.TOKEN_TYPE_CLAIM,
        "exp",
        api_settings.JTI_CLAIM,
        "jti",
    )
    access_token_class = AccessToken

    @property
    def access_token(self):
        access = self.access_token_class()
        access.set_exp(from_time=self.current_time)

        no_copy = self.no_copy_claims
        for claim, value in self.payload.items():
            if claim in no_copy:
                continue
            access[claim] = value

        return access

