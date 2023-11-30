from django.urls import path

from .api import RedirectAPIView

app_name = "redirect"

urlpatterns = [
    path("api/v1/redirect", RedirectAPIView.as_view(), name="redirect"),
]
