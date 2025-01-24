import os
from datetime import timedelta
from pathlib import Path

import sentry_sdk
from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent.parent


# -----------------------------------------------------------------------------
# Basic Config
# -----------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
DEBUG = config("DEBUG", default=False, cast=bool)


# -----------------------------------------------------------------------------
# Time & Language
# -----------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# -----------------------------------------------------------------------------
# Security and Users
# -----------------------------------------------------------------------------
SECRET_KEY = config("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", cast=Csv())
AUTH_USER_MODEL = "accounts.User"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# -----------------------------------------------------------------------------
# Databases
# -----------------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DJANGO_DB_NAME", "postgres"),
        "USER": os.getenv("DJANGO_DB_USER", "postgres"),
        "PASSWORD": os.getenv("DJANGO_DB_PASSWORD", "postgres"),
        "HOST": os.getenv("DJANGO_DB_HOST", "postgres"),
        "PORT": os.getenv("DJANGO_DB_PORT", "5432"),
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# -----------------------------------------------------------------------------
# Applications configuration
# -----------------------------------------------------------------------------
DEFAULT_APPS = [
    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
]

EXTERNAL_APPS = [
    "site",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "django_filters",
    "knox",
    "django_celery_beat",
    "django_celery_results",
    "drf_spectacular",
    "django_extensions",
]
CUSTOM_APPS = [
    "apps.accounts",
    "apps.organization",
    "apps.core",
    "apps.ai_models",
]

INSTALLED_APPS = DEFAULT_APPS + EXTERNAL_APPS + CUSTOM_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
CSRF_TRUSTED_ORIGINS = ["http://0.0.0.0:3000"]
CSRF_COOKIE_SECURE = True
SITE_ID = 1
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# -----------------------------------------------------------------------------
# Rest Framework
# -----------------------------------------------------------------------------
REST_KNOX = {
    "SECURE_HASH_ALGORITHM": "hashlib.sha512",
    "AUTH_TOKEN_CHARACTER_LENGTH": 64,
    "TOKEN_TTL": timedelta(hours=10),
    "USER_SERIALIZER": "apps.accounts.api.v1.serializers.UserProfileSerializer",
    "TOKEN_LIMIT_PER_USER": None,
    "AUTO_REFRESH": False,
    "AUTO_REFRESH_MAX_TTL": None,
    "MIN_REFRESH_INTERVAL": 60,
    "AUTH_HEADER_PREFIX": "Bearer",
    "TOKEN_MODEL": "knox.AuthToken",
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("knox.auth.TokenAuthentication",),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# TODO ⚡ Update the settings for the DRF Spectacular
SPECTACULAR_SETTINGS = {
    "TITLE": "Django Starter Template",
    "DESCRIPTION": "A comprehensive starting point for your new API with Django and DRF",
    "VERSION": "0.1.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

CORS_ALLOW_ALL_ORIGINS = True
REDIS_URL = config("REDIS_URL")
# -----------------------------------------------------------------------------
# Cache
# -----------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

USER_AGENTS_CACHE = "default"


# -----------------------------------------------------------------------------
# Celery
# -----------------------------------------------------------------------------
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", default="django-db")
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "America/Santiago"
CELERY_RESULT_EXTENDED = True


# -----------------------------------------------------------------------------
# Email
# -----------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True)
EMAIL_PORT = config("EMAIL_PORT", default=587)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")


# -----------------------------------------------------------------------------
# Sentry and logging
# -----------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "simple": {
            "format": "{asctime} {levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "apps.core.logging.handler.LoggingHandler",
            "filename": BASE_DIR / "debug.log",
            "formatter": "simple",
            "backupCount": 10,
            "maxBytes": 1 * 1024 * 1024,  # 1 MB
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": [
                "console",
            ],
            "level": "ERROR",
            "propagate": False,
        },
        "apps": {
            "handlers": [
                "console",
            ],
            "level": "INFO",
        },
    },
}

if not DEBUG:
    sentry_sdk.init(
        dsn=config("SENTRY_DSN"),
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )


# -----------------------------------------------------------------------------
# Static & Media Files
# -----------------------------------------------------------------------------
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

STATIC_URL = "/static/"
STATICFILES_DIRS = []
STATIC_ROOT = "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = "media"
ADMIN_MEDIA_PREFIX = STATIC_URL + "admin/"
