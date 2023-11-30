"""
Wisemen auto-generated settings for {project_name} project.
Please leave this intact, and overwrite or append below.
"""
from wisemen.settings.settings import *

ROOT_URLCONF = "{project_name}.urls"
WAGTAIL_SITE_NAME = "{project_name}"

# Project specific settings below:
LANGUAGE_CODE = "nl"
LANGUAGES = [
    ("nl", "Dutch"),
]

WAGTAIL_CONTENT_LANGUAGES = LANGUAGES

INSTALLED_APPS = INSTALLED_APPS + []

# Django Allauth settings, please see https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_VERIFICATION = "none"

# Append project specific renditions to be auto-generated.
PRERENDERED_IMAGE_RENDITIONS = PRERENDERED_IMAGE_RENDITIONS + [
    # Add your own image renditions here.
]