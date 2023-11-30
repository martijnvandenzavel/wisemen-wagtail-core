from dj_rest_auth.views import LogoutView as BaseLogoutView
from dj_rest_auth.jwt_auth import unset_jwt_cookies
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutView(BaseLogoutView):
    """
    Overriden LogoutView to mitigate problem with dj_rest_auth and the JWT Blacklist app.
    """

    def post(self, request, *args, **kwargs):
        return self.logout(request)

    def logout(self, request):
        response = Response(
            {"detail": "Successfully logged out."},
            status=status.HTTP_200_OK,
        )

        cookie_name = getattr(settings, "JWT_AUTH_REFRESH_COOKIE", None)

        unset_jwt_cookies(response)

        if cookie_name and cookie_name in request.COOKIES:
            token = RefreshToken(request.COOKIES.get(cookie_name))
            token.blacklist()

        return response
