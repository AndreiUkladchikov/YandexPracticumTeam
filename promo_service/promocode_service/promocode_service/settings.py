from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings, Field, RedisDsn


load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent


class SettingsFromEnv(BaseSettings):

    secret_key: str = Field(...)
    debug: bool = Field(False)
    allowed_hosts: str = Field(...)
    csrf_trusted_origins: str = Field(...)
    internal_ips: str = Field(...)

    db_name: str = Field(...)
    db_user: str = Field(...)
    db_password: str = Field(...)
    db_host: str = Field(...)
    db_port: int = Field(5432)

    celery_broker_url: RedisDsn = Field(...)
    celery_result_backend: RedisDsn = Field(...)

    django_log_level: str = Field("INFO")

    class Config:

        env_file = str(BASE_DIR / ".env")
        env_file_encoding = "utf-8"
        case_sensitive = False


config = SettingsFromEnv()


SECRET_KEY = config.secret_key
DEBUG = config.debug

ALLOWED_HOSTS = config.allowed_hosts.split(",")
CSRF_TRUSTED_ORIGINS = config.csrf_trusted_origins.split(",")

# allow internal ips when debug on
INTERNAL_IPS = config.internal_ips.split(",") if DEBUG else []


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "import_export",
    "rangefilter",
    "promocode",
    "django_extensions",
]

# remove debug_toolbar from installed apps when debug off
if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# remove debug_toolbar from middleware when debug off
if not DEBUG:
    MIDDLEWARE.pop(0)

ROOT_URLCONF = "promocode_service.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "promocode_service.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config.db_name,
        "USER": config.db_user,
        "PASSWORD": config.db_password,
        "HOST": config.db_host,
        "PORT": config.db_port,
        "OPTIONS": {"options": "-c search_path=public", }
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# DRF settings
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
}

# Swagger settings
SPECTACULAR_SETTINGS = {
    "TITLE": "Promocode API",
    "DESCRIPTION": "API schema for Promocode service",
    "VERSION": "1.0.0",
    "SWAGGER_UI_DIST": "SIDECAR",  # shorthand to use the sidecar instead
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    # OTHER SETTINGS
}

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

TIME_ZONE = "Europe/Moscow"
USE_TZ = True
LANGUAGE_CODE = "ru-RU"
USE_I18N = True
USE_L10N = True
LOCALE_PATHS = ["promocode_service/locale", ]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = "./static"

MEDIA_URL = "media/"
MEDIA_ROOT = "./media"

# Django logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {asctime} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": config.django_log_level,
            "propagate": False,
        },
    },
}

IMPORT_EXPORT_USE_TRANSACTIONS = True

CELERY_BROKER_URL = config.celery_broker_url
CELERY_RESULT_BACKEND = config.celery_result_backend
