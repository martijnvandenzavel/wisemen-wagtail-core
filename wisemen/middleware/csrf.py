from django.utils.deprecation import MiddlewareMixin


class DisableCSRF(MiddlewareMixin):
    """
    Disable CSRF checks for the API.
    """
    @staticmethod
    def process_request(request):
        setattr(request, '_dont_enforce_csrf_checks', True)
