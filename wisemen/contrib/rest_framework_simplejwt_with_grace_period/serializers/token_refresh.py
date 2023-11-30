from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from rest_framework_simplejwt_with_grace_period.models.refresh import RefreshWithGracePeriodToken


class TokenRefreshWithGracePeriodSerializer(TokenRefreshSerializer):
    """
    Small override of the original TokenRefreshSerializer to set our
    own token_class to RefreshWithGracePeriodToken.
    """
    token_class = RefreshWithGracePeriodToken
