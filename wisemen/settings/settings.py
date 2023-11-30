import os
from datetime import timedelta

import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.rq import RqIntegration

ENV = environ.Env()

# properly parse boolean flags to set DEBUG and DEBUG_PROPAGATE_EXCEPTIONS
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
DEBUG_PROPAGATE_EXCEPTIONS = os.getenv("DEBUG_PROPAGATE_EXCEPTIONS", "False").lower() in (
    "true",
    "1",
    "t",
)

PROJECT_DIR = os.path.dirname(ENV("PROJECT_DIR"))
BASE_DIR = os.path.dirname(PROJECT_DIR)  # Parent directory of project directory.

SECRET_KEY = ENV("SECRET_KEY")
ALLOWED_HOSTS = ENV("ALLOWED_HOSTS").split()

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Applications definition
INSTALLED_APPS = [
    "wisemen",
    "daphne",
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "dj_rest_auth",
    "django_rest_passwordreset",
    "django_filters",
    "corsheaders",
    "generic_chooser",
    "wagtailcolumnblocks",
    "wagtailseo",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.settings",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "wagtail_localize",
    "wagtail_localize.modeladmin",
    "wagtail_localize.locales",
    "wagtailorderable",
    "modelcluster",
    "taggit",
    "wagtailvideos",
    "drf_spectacular",
    "django_rq",
    "django_db_logger",
    "wisemen.contrib.multilingual_sitemap",
    "wisemen.contrib.rest_framework_simplejwt_with_grace_period",
    "wisemen.contrib.redirect",
]

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "wisemen.middleware.csrf.DisableCSRF",  # Disable CSRF for API
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(ENV("PROJECT_DIR"), "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "wagtail.contrib.settings.context_processors.settings",
            ],
        },
    },
]

# Set up a database logger for direct use.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        },
        "simple": {"format": "%(levelname)s %(asctime)s %(message)s"},
    },
    "handlers": {
        "db_log": {"level": "DEBUG", "class": "django_db_logger.db_log_handler.DatabaseLogHandler"},
    },
    "loggers": {
        "db": {"handlers": ["db_log"], "level": "DEBUG"},
    },
}

# Prepare both a WSGI and ASGI application.
WSGI_APPLICATION = "wisemen.wsgi.application"
ASGI_APPLICATION = "wisemen.asgi.application"

# Set up internationalization.
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
WAGTAIL_I18N_ENABLED = True
WAGTAIL_LOCALIZE_DEFAULT_TRANSLATION_MODE = "simple"  # Force async translations.
SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/4.1/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(PROJECT_DIR, "static_files")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(PROJECT_DIR, "media")
MEDIA_URL = "/media/"

# Set up a default file based cache, so it can be used tro cache certain API view outputs.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': ENV("FILE_CACHE_LOCATION"),
        'TIMEOUT': 60,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    },
    'redis': {
        'BACKEND': 'django_redis.cache.RedisCache',
        "LOCATION": f'redis://{ENV("REDIS_HOST")}:{ENV("REDIS_PORT")}/1',
        "OPTIONS": {
             "PASSWORD": ENV("REDIS_PASS"),
             "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "wagtail"
    }
}

# Set up a default search backend.
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = ENV("WAGTAILADMIN_BASE_URL")

# Generic AWS settings.
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_ACCESS_KEY_ID = ENV("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = ENV("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = ENV("AWS_STORAGE_BUCKET_NAME")
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_DEFAULT_ACL = "public-read"
AWS_S3_FILE_OVERWRITE = False  # Allow for autorenaming files with the same filename.
AWS_QUERYSTRING_AUTH = False  # Don't sign all files in Boto3.
# Private file storage.
AWS_PRIVATE_LOCATION = ENV("AWS_S3_PRIVATE_STORAGE_BASE")
AWS_PRIVATE_FILE_STORAGE = (
    "wisemen.storage_backends.PrivateMediaStorage"  # Custom storage class for private files.
)
AWS_LOCATION = ENV("AWS_S3_PUBLIC_STORAGE_BASE")
AWS_S3_ENDPOINT_URL = ENV("AWS_S3_ENDPOINT_URL")
AWS_S3_REGION_NAME = ENV("AWS_S3_REGION_NAME")
S3_BASE_URL = "%s/%s" % (AWS_S3_ENDPOINT_URL, AWS_LOCATION)

# Enable Sentry for all environments except local.
if ENV("SENTRY_ENVIRONMENT") != "local":
    sentry_sdk.init(
        dsn=ENV("SENTRY_DSN"),
        integrations=[DjangoIntegration(), RedisIntegration(), RqIntegration()],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=0.05,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
        environment=ENV("SENTRY_ENVIRONMENT"),
    )

# Load in all allowed origins for CORS.
CORS_ALLOWED_ORIGINS = ENV("CORS_ALLOWED_ORIGINS").split()

AUTHENTICATION_BACKENDS = [
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Set up DRF with JWT authentication and a few sane defaults.
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "COERCE_DECIMAL_TO_STRING": True,
    "PAGE_SIZE": 10,
}

REST_AUTH = {
    "USE_JWT": True,
    "TOKEN_MODEL": None,
    "JWT_AUTH_COOKIE": "jwt-access-token",
    "JWT_AUTH_REFRESH_COOKIE": "jwt-refresh-token",
}

# Setup simple JWT handling with a grace period for token refreshes.
SIMPLE_JWT = {
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(weeks=1),
    "REFRESH_TOKEN_GRACE_PERIOD": timedelta(seconds=10),
    "TOKEN_OBTAIN_SERIALIZER": "user_profile.serializers.UserProfileTokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "wisemen.rest_framework_simplejwt_with_grace_period.serializers.TokenRefreshWithGracePeriodSerializer",
}

# Set up account related settings.
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_ADAPTER = "wisemen.adaptors.AccountAdapter"

# Set up a PostgreSQL database backend with PostGIS included by default.
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": ENV("DATABASE_NAME"),
        "USER": ENV("DATABASE_USER"),
        "PASSWORD": ENV("DATABASE_PASS"),
        "HOST": ENV("DATABASE_HOST"),  # Set to empty string for localhost.
        "PORT": ENV("DATABASE_PORT"),  # Set to empty string for default.
        "CONN_MAX_AGE": 600,  # number of seconds database connections should persist for
        "DISABLE_SERVER_SIDE_CURSORS": True,  # Mitiagte issues with server side cursors while using PGBouncer in "transaction" mode
    }
}

ROOT_URLCONF = f"{ENV('SITE_MODULE_NAME')}.urls"
WAGTAIL_SITE_NAME = ENV("WAGTAIL_SITE_NAME")
WAGTAILDOCS_SERVE_METHOD = "direct"

# If there is an issue with gdal/geos not finding the right libraries, add these to .envrc file
# Use sudo find / -name libgeos_c.dylib in a terminal window and specify the path to the libgdal.dylib and libgeos_c.dylib
# Note: If pointing to "/opt/homebrew/lib/libgeos_c.dylib" make sure you have postgis installed via brew (brew install postgis)
if "GDAL_LIBRARY_PATH" in ENV:
    GDAL_LIBRARY_PATH = ENV("GDAL_LIBRARY_PATH")
if "GEOS_LIBRARY_PATH" in ENV:
    GEOS_LIBRARY_PATH = ENV("GEOS_LIBRARY_PATH")


# Set up the email backend and settings.
EMAIL_BACKEND = ENV("EMAIL_BACKEND")
if "EMAIL_HOST" in ENV:
    EMAIL_HOST = ENV("EMAIL_HOST")
if "EMAIL_PORT" in ENV:
    EMAIL_PORT = ENV("EMAIL_PORT")
if "EMAIL_HOST_PASSWORD" in ENV:
    EMAIL_HOST_PASSWORD = ENV("EMAIL_HOST_PASSWORD")
if "EMAIL_HOST_USER" in ENV:
    EMAIL_HOST_USER = ENV("EMAIL_HOST_USER")

# Set up Django RQ.
RQ_QUEUES = {
    ENV("REDIS_QUEUE"): {
        "HOST": ENV("REDIS_HOST"),
        "PORT": ENV("REDIS_PORT"),
        "DB": 0,
        "PASSWORD": ENV("REDIS_PASS"),
        "DEFAULT_TIMEOUT": 360,
    }
}

WS_PROTOCOL = ENV("WS_PROTOCOL")

# Default image renditions that should be geenrated when saving a new image.
# These are based on Wagtai's renditions used in the admin.
PRERENDERED_IMAGE_RENDITIONS = [
    "original",
    "max-800x600",
    "max-165x165"
]