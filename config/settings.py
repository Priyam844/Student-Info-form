"""Django settings for the supabase_students project.

Database selection is driven by environment variables (see .env):

    SUPABASE_DB_URL / DATABASE_URL  ->  connect to Supabase Postgres
    (missing)                       ->  fall back to local SQLite so the
                                        project still runs before you
                                        have Supabase credentials.
"""

import os
from pathlib import Path
from urllib.parse import parse_qsl, unquote, urlparse

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-dev-only-key-change-me")

DEBUG = os.getenv("DJANGO_DEBUG", "True").strip().lower() in {"1", "true", "yes"}

# ALLOWED_HOSTS = [
#     host.strip()
#     for host in os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
#     if host.strip()
# ]
ALLOWED_HOSTS = [
    "student-info-form.onrender.com",
    "localhost",
    "127.0.0.1",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "students",
]

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

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


def build_database_config() -> dict:
    """Turn a Supabase/Postgres connection string into Django DB settings."""
    url = (os.getenv("SUPABASE_DB_URL") or os.getenv("DATABASE_URL") or "").strip()

    if not url:
        print(
            "[config] SUPABASE_DB_URL not set -> using local SQLite "
            "(db.sqlite3). Add it to .env to switch to Supabase."
        )
        return {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        }

    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]

    parsed = urlparse(url)
    if parsed.scheme not in {"postgresql", "postgresql+psycopg2"} or not parsed.hostname:
        raise ImproperlyConfigured(
            "SUPABASE_DB_URL must look like "
            "postgresql://USER:PASSWORD@HOST:PORT/postgres"
        )

    query = dict(parse_qsl(parsed.query))

    options = {"sslmode": query.get("sslmode", "require")}

    return {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": unquote(parsed.path.lstrip("/")) or "postgres",
            "USER": unquote(parsed.username or ""),
            "PASSWORD": unquote(parsed.password or ""),
            "HOST": parsed.hostname,
            "PORT": str(parsed.port or 5432),
            "OPTIONS": options,
            "CONN_MAX_AGE": 60,
            "CONN_HEALTH_CHECKS": True,
            "ATOMIC_REQUESTS": False,
        }
    }



DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = os.getenv("DJANGO_TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
