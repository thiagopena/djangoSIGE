"""Django settings for DjangoSIGE project."""

from pathlib import Path

from decouple import Csv, config
from dj_database_url import parse as dburl

# Core Settings
################################################################################
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

# Debuging
################################################################################
DEBUG = config("DEBUG", cast=bool)

# Database
################################################################################
try:
    DATABASES = {"default": config("DATABASE_URL", cast=dburl)}
except ValueError:
    DATABASES = {
        "default": {
            "ENGINE": config("SQL_ENGINE"),
            "NAME": config("SQL_DB"),
            "USER": config("SQL_USER"),
            "PASSWORD": config("SQL_PASSWORD"),
            "HOST": config("SQL_HOST"),
            "PORT": config("SQL_PORT"),
        }
    }
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# Email
################################################################################
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_USE_TLS = config("EMAIL_USE_TLS")

# File Uploads
################################################################################
MEDIA_ROOT = str(BASE_DIR / "djangosige/mediafiles/")
MEDIA_URL = "media/"

# Globalization
################################################################################
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# HTTP
################################################################################
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "djangosige.middleware.LoginRequiredMiddleware",
]
WSGI_APPLICATION = "config.wsgi.application"

# Models
################################################################################
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "djangosige.base",
    "djangosige.login",
    "djangosige.cadastro",
    "djangosige.vendas",
    "djangosige.compras",
    "djangosige.fiscal",
    "djangosige.financeiro",
    "djangosige.estoque",
]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Security
################################################################################
SECRET_KEY = config("SECRET_KEY")
X_FRAME_OPTIONS = "DENY"

# Serialization
################################################################################
DEFAULT_CHARSET = "utf-8"

# Templates
################################################################################
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "djangosige/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "djangosige.base.context_version.sige_version",
                "djangosige.login.context_user.foto_usuario",
            ],
        },
    },
]

# Testing
################################################################################
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# URLs
################################################################################
ROOT_URLCONF = "config.urls"

# Auth
################################################################################
AUTH_USER_MODEL = "auth.User"
LOGIN_REDIRECT_URL = ""
LOGIN_URL = ""
LOGOUT_REDIRECT_URL = ""
LOGIN_NOT_REQUIRED = (
    r"^/login/$",
    r"/login/esqueceu/",
    r"/login/trocarsenha/",
    r"/logout/",
)
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

# Sessions
################################################################################
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Static Files
################################################################################
STATIC_ROOT = str(BASE_DIR / "staticfiles")
STATIC_URL = "static/"
STATICFILES_DIRS = [str(BASE_DIR / "djangosige/static")]
